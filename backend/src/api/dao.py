import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.utils.hasher import get_message_hash
from src.utils.files import create_file, get_from_file
from src.core.models import Message
from src.core.config import BASE_DIR, settings
from src.exceptions.files import FileCreateException, FileReadException

MESSAGES_DIR = BASE_DIR / "messages"


def _get_storage_size() -> int:
    total = 0
    try:
        with os.scandir(MESSAGES_DIR) as entries:
            for entry in entries:
                if entry.is_file():
                    total += entry.stat().st_size
    except FileNotFoundError:
        pass
    return total


async def _evict_oldest(session: AsyncSession, bytes_to_free: int) -> None:
    freed = 0
    oldest = select(Message).order_by(Message.id.asc())
    result = await session.execute(oldest)
    for msg in result.scalars():
        if freed >= bytes_to_free:
            break
        try:
            size = os.path.getsize(msg.message_path)
            os.remove(msg.message_path)
            freed += size
        except OSError:
            pass
        await session.delete(msg)
    await session.flush()


async def message_create(message: str, secret_key: str, session: AsyncSession) -> str:
    message_hash = get_message_hash(message, secret_key)
    path = str(MESSAGES_DIR / f"{message_hash}.txt")

    message_bytes = len(message.encode("utf-8"))
    storage_used = _get_storage_size()
    if storage_used + message_bytes > settings.max_storage_bytes:
        overflow = storage_used + message_bytes - settings.max_storage_bytes
        await _evict_oldest(session, overflow)

    entity = Message(
        message_path=path, message_hash=message_hash, message_salt=secret_key
    )

    try:
        await create_file(path, message)
        session.add(entity)
        await session.commit()

        return message_hash

    except Exception as e:
        print(e)
        raise FileCreateException


async def message_get(
    message_hash: str, secret_key: str, session: AsyncSession
) -> str | None:
    query = select(Message).where(
        Message.message_hash == message_hash, Message.message_salt == secret_key
    )
    result = await session.execute(query)

    message: Message | None = result.scalars().one_or_none()

    if message is None:
        return None

    try:
        text = await get_from_file(message.message_path)
    except Exception as e:
        print(e)
        raise FileReadException

    return text

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.utils.hasher import get_message_hash
from src.utils.files import create_file, get_from_file
from src.core.models import Message
from src.core.config import BASE_DIR
from src.exceptions.files import FileCreateException, FileReadException


async def message_create(message: str, secret_key: str, session: AsyncSession) -> str:
    message_hash = get_message_hash(message, secret_key)
    path = str(BASE_DIR / "messages" / f"{message_hash}.txt")

    entity = Message(
        message_path=path, message_hash=message_hash, message_salt=secret_key
    )

    try:
        await create_file(path, message)
    except Exception as e:
        print(e)
        raise FileCreateException

    session.add(entity)
    await session.commit()

    return message_hash


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

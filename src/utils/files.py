from aiofile import async_open
from src.core.config import BASE_DIR


async def get_from_file(path: str) -> str:
    async with async_open(path, "rb") as file:
        text = await file.read()
        file.seek(0)
        return text.decode()


async def create_file(path: str, text: str) -> None:
    async with async_open(path, "wb") as file:
        await file.write(text.encode())
        file.seek(0)

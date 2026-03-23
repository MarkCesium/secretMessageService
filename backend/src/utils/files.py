from aiofile import async_open


async def get_from_file(path: str) -> str:
    async with async_open(path, "rb") as file:
        text: bytes = await file.read()
        return text.decode()


async def create_file(path: str, text: str) -> None:
    async with async_open(path, "wb") as file:
        await file.write(text.encode())

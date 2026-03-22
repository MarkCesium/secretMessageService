from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from src.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=False,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper: DatabaseHelper = DatabaseHelper(
    settings.db_url,
)

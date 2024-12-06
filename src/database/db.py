from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import settings


async_engine = create_async_engine(url=settings.DATABASE_URL)
SESSION_FACTORY = async_sessionmaker(bind=async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SESSION_FACTORY() as session:
        yield session

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

engine = create_async_engine(str(settings.db_uri))

if "asyncpg" not in str(engine.url):
    raise ValueError("Only async mode is supported")

session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


Base: DeclarativeMeta = declarative_base()

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

# POSTGRES_INDEXES_NAMING_CONVENTION = {
#     "ix": "%(column_0_label)s_idx",
#     "uq": "%(table_name)s_%(column_0_name)s_key",
#     "ck": "%(table_name)s_%(constraint_name)s_check",
#     "fk": "%(table_name)s_%(column_0_name)s_fkey",
#     "pk": "%(table_name)s_pkey",
# }
#
# metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
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

from __future__ import annotations

import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy import UUID, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declarative_base, declared_attr, mapped_column, sessionmaker


def get_uri() -> str:
    from core.config import settings

    return str(settings.db_uri)


engine = create_async_engine(get_uri(), future=True)

if "asyncpg" not in str(engine.url):
    raise ValueError("Only async mode is supported")

session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


Base = declarative_base()


class BaseManager:
    _model: Base

    def __init__(self, model):
        self._model = model

    async def get_by_id(self, id):
        async with session_maker() as session:
            query = select(self._model).filter_by(id=id)
            instance = await session.execute(query)
            instance = instance.scalar()
            if instance:
                return instance
            else:
                raise self._model.NotFoundError(f"{self._model.__name__} with id {id} not found")

    async def get(self, **kwargs):
        async with session_maker() as session:
            query = select(self._model).filter_by(**kwargs)
            instance = await session.execute(query)
            instance = instance.scalars().all()
            if len(instance) > 1:
                raise self._model.MultipleObjectsReturned(f"Multiple {self._model.__name__} with {kwargs} found")
            if instance:
                return instance[0]
            else:
                raise self._model.NotFoundError(f"{self._model.__name__} with {kwargs} not found")

    async def all(self):
        async with session_maker() as session:
            query = select(self._model)
            instances = await session.execute(query)
            return instances.scalars().all()

    async def filter(self, **kwargs):
        async with session_maker() as session:
            query = select(self._model).filter_by(**kwargs)
            instances = await session.execute(query)
            return instances.scalars().all()

    async def get_or_create(self, **kwargs) -> tuple[type[BaseModel], bool]:
        async with session_maker() as session:
            query = select(self._model).filter_by(**kwargs)
            instance = await session.execute(query)
            instance = instance.scalar()
            if instance:
                return instance, False
            instance = self._model(**kwargs)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance, True

    async def update_or_create(self, **kwargs) -> tuple[type[BaseModel], bool]:
        async with session_maker() as session:
            query = select(self._model).filter_by(**kwargs)
            instance = await session.execute(query)
            instance = instance.scalar()
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                await session.commit()
                session.refresh(instance)
                return instance, False
            instance = self._model(**kwargs)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance, True

    async def create(self, **kwargs):
        async with session_maker() as session:
            instance = self._model(**kwargs)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @staticmethod
    async def bulk_create(instances):
        async with session_maker() as session:
            session.add_all(instances)
            await session.commit()
            return instances


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    class NotFoundError(Exception):
        pass

    class MultipleObjectsReturned(Exception):
        pass

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    @declared_attr
    def objects(cls):
        return BaseManager(cls)

    @property
    def _session(self):
        return session_maker

    @hybrid_property
    def pk(self) -> uuid.UUID:
        return self.id

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    async def save(self) -> BaseModel:
        async with self._session() as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
        return self

    async def delete(self):
        async with self._session() as session:
            await session.delete(self)
            await session.commit()
        del self

    async def update(self, **kwargs):
        async with self._session() as session:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.add(self)
            await session.commit()
            await session.refresh(self)

    async def refresh(self):
        async with self._session() as session:
            await session.refresh(self)

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__table__.columns.keys()}

import uuid
from collections.abc import AsyncGenerator
from datetime import datetime

from config import get_settings
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

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


class BaseModel:
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # def save(self):
    #     with session_maker() as session:
    #         session.add(self)
    #         session.commit()
    #         session.refresh(self)
    #         return self
    #
    # def delete(self):
    #     with session_maker() as session:
    #         session.delete(self)
    #         session.commit()
    #         del self
    #
    # def update(self, **kwargs):
    #     with session_maker() as session:
    #         for key, value in kwargs.items():
    #             setattr(self, key, value)
    #         session.commit()
    #         session.refresh(self)
    #         return self
    #
    # @classmethod
    # def get(cls, id):
    #     with session_maker() as session:
    #         return session.query(cls).get(id)
    #
    # @classmethod
    # def all(cls):
    #     with session_maker() as session:
    #         return session.query(cls).all()
    #
    # @classmethod
    # def filter(cls, **kwargs):
    #     with session_maker() as session:
    #         return session.query(cls).filter_by(**kwargs).all()
    #
    # @classmethod
    # def get_or_create(cls, **kwargs):
    #     with session_maker() as session:
    #         instance = session.query(cls).filter_by(**kwargs).first()
    #         if instance:
    #             return instance
    #         instance = cls(**kwargs)
    #         session.add(instance)
    #         session.commit()
    #         session.refresh(instance)
    #         return instance
    #
    # @classmethod
    # def update_or_create(cls, **kwargs):
    #     with session_maker() as session:
    #         instance = session.query(cls).filter_by(**kwargs).first()
    #         if instance:
    #             for key, value in kwargs.items():
    #                 setattr(instance, key, value)
    #             session.commit()
    #             session.refresh(instance)
    #             return instance
    #         instance = cls(**kwargs)
    #         session.add(instance)
    #         session.commit()
    #         session.refresh(instance)
    #         return
    #
    # @classmethod
    # def create(cls, **kwargs):
    #     with session_maker() as session:
    #         instance = cls(**kwargs)
    #         session.add(instance)
    #         session.commit()
    #         session.refresh(instance)
    #         return instance
    #
    # @classmethod
    # def delete(cls, id):
    #     with session_maker() as session:
    #         instance = session.query(cls).get(id)
    #         if instance:
    #             session.delete(instance)
    #             session.commit()
    #             return instance
    #         return None
    #
    # @classmethod
    # def bulk_create(cls, instances):
    #     with session_maker() as session:
    #         session.bulk_save_objects(instances)
    #         session.commit()
    #         return instances
    #
    # @classmethod
    # def bulk_delete(cls, ids):
    #     with session_maker() as session:
    #         instances = session.query(cls).filter(cls.id.in_(ids)).all()
    #         session.delete(instances)
    #         session.commit()
    #         return instances
    #
    # @classmethod
    # def bulk_update(cls, ids, **kwargs):
    #     with session_maker() as session:
    #         instances = session.query(cls).filter(cls.id.in_(ids)).all()
    #         for instance in instances:
    #             for key, value in kwargs.items():
    #                 setattr(instance, key, value)
    #         session.commit()
    #         return instances
    #
    # @classmethod
    # def bulk_get(cls, ids):
    #     with session_maker() as session:
    #         return session.query(cls).filter(cls.id.in_(ids)).all()
    #
    # @classmethod
    # def bulk_filter(cls, **kwargs):
    #     with session_maker() as session:
    #         return session.query(cls).filter_by(**kwargs).all()
    #
    #
    # @classmethod
    # def bulk_get_or_create(cls, **kwargs):
    #     with session_maker() as session:
    #         instances = session.query(cls).filter_by(**kwargs).all()
    #         if instances:
    #             return instances
    #         instances = [cls(**kwargs) for _ in range(len(kwargs))]
    #         session.bulk_save_objects(instances)
    #         session.commit()
    #         return instances

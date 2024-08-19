import uuid
from enum import Enum

from core.config.db import BaseModel
from sqlalchemy import JSON, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import StatusEnum


class YTChannelModel(BaseModel):
    __tablename__ = "channels"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None, lazy="immediate")

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None, lazy="immediate")

    meta_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[Enum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.new, index=True)
    ext_id: Mapped[str] = mapped_column(index=True, unique=True)


class YTPlaylistModel(BaseModel):
    __tablename__ = "playlists"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None, lazy="immediate")

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None, lazy="immediate")

    meta_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[Enum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.new, index=True)
    ext_id: Mapped[str] = mapped_column(index=True, unique=True)


class YTVideoModel(BaseModel):
    __tablename__ = "videos"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None, lazy="immediate")

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None, lazy="immediate")

    meta_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[Enum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.new, index=True)
    ext_id: Mapped[str] = mapped_column(index=True, unique=True)

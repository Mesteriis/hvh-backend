import uuid

from config.db import Base, BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class YTChannel(Base, BaseModel):
    __tablename__ = "channels"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None)


class YTPlaylist(Base, BaseModel):
    __tablename__ = "playlists"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None)


class YTVideo(Base, BaseModel):
    __tablename__ = "videos"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates=None)

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from config.db import BaseModel, Base


class YTChannel(Base, BaseModel):
    __tablename__ = "channels"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE")
    )
    task: Mapped["Task"] = relationship("Task", back_populates=None)


class YTPlaylist(Base, BaseModel):
    __tablename__ = "playlists"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE")
    )
    task: Mapped["Task"] = relationship("Task", back_populates=None)


class YTVideo(Base, BaseModel):
    __tablename__ = "videos"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates=None)

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE")
    )
    task: Mapped["Task"] = relationship("Task", back_populates=None)

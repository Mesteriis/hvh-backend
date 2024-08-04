import uuid

from core.config.db import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    url: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="tasks")

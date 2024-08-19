import uuid
from enum import Enum

from core.config.db import BaseModel
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TaskStatusEnum(Enum):
    new = "new"
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    url: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="tasks")

    status: Mapped[Enum] = mapped_column(SqlEnum(TaskStatusEnum), default=TaskStatusEnum.new, index=True)

    def __repr__(self) -> str:
        return f"<TaskModel id={self.id} url={self.url} status={self.status}>"

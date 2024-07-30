import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from config.db import Base, BaseModel


class TaskModel(Base, BaseModel):
    __tablename__ = "tasks"

    url: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped['User'] = relationship("User", back_populates="tasks")



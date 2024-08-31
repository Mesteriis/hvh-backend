from __future__ import annotations

from datetime import datetime

from applications.users.auth.utils.password import get_password_hash
from core.config.db import BaseModel
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(BaseModel):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(1000), nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    date_joined: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tasks: Mapped[TaskModel] = relationship("TaskModel", back_populates="owner")

    async def set_password(self, password: str) -> None:
        self.hashed_password = get_password_hash(password=password)
        await self.save()

    async def check_password(self, password: str) -> bool:
        return get_password_hash(password) == self.hashed_password

    def __repr__(self) -> str:
        return f"<UserModel id={self.id} email={self.email} is_active={self.is_active}  date_joined={self.date_joined}>"

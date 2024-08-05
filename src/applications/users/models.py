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
    hashed_password: Mapped[str] = mapped_column(String(1000), nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    date_joined: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tasks: Mapped["TaskModel"] = relationship("TaskModel", back_populates="owner")

    @classmethod
    async def register_user(cls, user) -> UserModel:
        user_dict = user.model_dump()
        password_hash = get_password_hash(password=user.password)
        model = cls(**user_dict, password_hash=password_hash)
        await model.save()
        return model

    async def set_password(self, password: str) -> None:
        self.password_hash = get_password_hash(password=password)
        await self.save(update_fields=["password_hash"])

from __future__ import annotations

import uuid

from applications.users.auth.utils.password import get_password_hash
from tools.base_db_model import BaseDBModel
from tortoise import fields


class UserModel(BaseDBModel):
    id = fields.UUIDField(pk=True, index=True, unique=True, null=False, default=lambda: str(uuid.uuid4()))
    email = fields.CharField(max_length=256, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    hashed_password = fields.CharField(max_length=1000, null=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    date_joined = fields.DatetimeField(auto_now_add=True)

    async def set_password(self, password: str) -> None:
        self.hashed_password = get_password_hash(password=password)
        await self.save()

    async def check_password(self, password: str) -> bool:
        return get_password_hash(password) == self.hashed_password

    def __repr__(self) -> str:
        return f"<UserModel id={self.id} email={self.email} is_active={self.is_active}  date_joined={self.date_joined}>"

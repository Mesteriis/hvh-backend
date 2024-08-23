from uuid import UUID

from applications.users.models import UserModel
from fastapi import HTTPException


class UserSelector:
    @classmethod
    async def get_user_by_uid(cls, user_uid: UUID | str) -> UserModel:
        return await UserModel.objects.get(id=user_uid)

    @classmethod
    async def get_by_email(cls, email: str) -> UserModel:
        return await UserModel.objects.get(email=email)

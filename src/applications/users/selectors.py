from uuid import UUID

from applications.users.models import UserModel
from fastapi import HTTPException


class UserSelector:
    @staticmethod
    async def get_user_by_uid(user_uid: UUID | str) -> UserModel:
        try:
            return await UserModel.objects.get(id=user_uid)
        except UserModel.NotFoundError as e:
            raise HTTPException(status_code=404, detail="User not found") from e

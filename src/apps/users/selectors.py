from uuid import UUID

from fastapi import HTTPException

from apps.users.models import UserModel


class UserSelector:
    @staticmethod
    async def get_user_by_uid(user_uid: UUID | str) -> UserModel:
        try:
            return await UserModel.objects.get(id=user_uid)
        except UserModel.NotFoundError:
            raise HTTPException(status_code=404, detail="User not found")

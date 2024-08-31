from uuid import UUID

from applications.users.models import UserModel


class UserSelector:
    @classmethod
    async def get_by_uid(cls, user_uid: UUID | str) -> UserModel:
        return await UserModel.objects.get(id=user_uid)

    @classmethod
    async def get_by_email(cls, email: str) -> UserModel:
        return await UserModel.objects.get(email=email)

    @classmethod
    async def get_all(cls) -> list[UserModel]:
        return await UserModel.objects.all()

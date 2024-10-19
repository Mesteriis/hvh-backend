from uuid import UUID

from applications.users.models import UserModel


class UserSelector:
    FileNotFoundError = None

    @classmethod
    async def get_by_uid(cls, user_uid: UUID | str) -> UserModel:
        return await UserModel.get(id=user_uid)

    @classmethod
    async def get_by_email(cls, email: str) -> UserModel:
        return await UserModel.get(email=email)

    @classmethod
    async def get_all(cls) -> list[UserModel]:
        return await UserModel.all()

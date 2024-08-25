from uuid import UUID

from applications.users.auth.utils.contrib import verify_password_reset_token
from applications.users.models import UserModel
from applications.users.schemas import ResetPasswordSchema
from fastapi import HTTPException

from core.config import settings
from .auth.utils.password import get_password_hash
from .schemas.user_schemas import UserRegisterStruct, UserInBaseStruct
from .selectors import UserSelector


class UserInteractor:

    @classmethod
    async def update(cls, user_id,  user_data) -> UserModel:
        user_data: dict = user_data.model_dump(exclude_unset=True)
        user = await UserSelector.get_by_uid(user_id)
        await user.update(**user_data)
        return user

    @classmethod
    async def registry_user(cls, data: UserRegisterStruct) -> UserModel:
        try:
            await UserSelector.get_by_email(email=data.email)
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
        except UserModel.NotFoundError:
            user = await UserModel.objects.create(
                email=data.email,
                hashed_password=get_password_hash(password=data.password),
                is_active=settings.id_account_verification is False,
                is_superuser=False,
            )

            return user
    @classmethod
    async def block_user(cls, user_id: UUID) -> UserModel:
        user = await UserSelector.get_by_uid(user_id)
        if user.is_superuser:
            raise HTTPException(status_code=400, detail="You can't block superuser")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="User already blocked")
        user.is_active = False
        await user.save()
        return user

    @classmethod
    async def unblock_user(cls, user_id: UUID) -> UserModel:
        user = await UserSelector.get_by_uid(user_id)
        if user.is_superuser:
            raise HTTPException(status_code=400, detail="You can't unblock superuser")
        if user.is_active:
            raise HTTPException(status_code=400, detail="User already unblocked")
        user.is_active = True
        await user.save()
        return user


class PasswordInteractor:
    async def reset_password(self, payload: ResetPasswordSchema) -> None:
        reset_token = payload.reset_token
        email = verify_password_reset_token(reset_token)

        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = await UserSelector.get_by_email(email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system.",
            )
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        password = payload.password
        hashed_password = get_password_hash(password)
        user.password_hash = hashed_password
        await user.save(update_fields=("password_hash",))

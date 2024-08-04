from fastapi import HTTPException

from apps.users.auth.utils.contrib import verify_password_reset_token
from apps.users.models import UserModel
from apps.users.schemas import BaseUserUpdate, ResetPasswordSchema
from .auth.utils.password import get_password_hash
from .selectors import UserSelector

class UserInteractor:
    def __init__(self, user: UserModel):
        self.user = user

    async def update(self, user_data: BaseUserUpdate):
        user_data: dict = user_data.model_dump(exclude_unset=True)
        if "first_name" in user_data and not user_data.get("first_name"):
            raise HTTPException(
                status_code=400,
                detail="first_name is a required field.",
            )

        for key, value in user_data.items():
            setattr(self.user, key, value)

        await self.user.save()
        await self.user.refresh_from_db()
        return self.user



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

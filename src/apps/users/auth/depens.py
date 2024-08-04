import jwt
from fastapi import HTTPException
from fastapi import Security
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from apps.users.auth.schemas import JWTTokenPayload
from apps.users.auth.utils.contrib import reusable_oauth2
from apps.users.auth.utils.jwt import ALGORITHM
from apps.users.models import UserModel
from apps.users.selectors import UserSelector
from core.config import settings


async def current_user(token: str = Security(reusable_oauth2)) -> UserModel | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return await UserSelector.get_user_by_uid(token_data.user_id)


async def current_active_user(cur_user: UserModel = Security(current_user)):
    if not cur_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def current_superuser(cur_user: UserModel = Security(current_user)):
    if not cur_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

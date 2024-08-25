import jwt
from applications.users.auth.schemas import JWTTokenPayload
from applications.users.auth.utils.contrib import reusable_oauth2
from applications.users.auth.utils.jwt import ALGORITHM
from applications.users.models import UserModel
from applications.users.selectors import UserSelector
from core.config import settings
from fastapi import HTTPException, Security
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN


async def current_user(token: str = Security(reusable_oauth2)) -> UserModel | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except PyJWTError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials") from e
    try:
        user = await UserSelector.get_by_uid(token_data.user_id)
    except UserModel.NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def superuser(token: str = Security(reusable_oauth2)) -> UserModel | None:
    user = await current_user(token)
    if user.is_superuser is False:
        raise HTTPException(status_code=403, detail="The user does not have enough privileges")
    return user
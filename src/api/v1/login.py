from applications.auth.schemas import CredentialsSchema, JWTPairToken, RefreshJWTToken
from applications.auth.utils.contrib import authenticate
from applications.auth.utils.jwt import (
    get_jwt_pair_from_user,
    get_jwt_pair_with_userid_from_refresh_token,
)
from applications.users.utils import update_last_login
from fastapi import APIRouter, HTTPException

login_router = APIRouter()


@login_router.post("/access-token", response_model=JWTPairToken, tags=["auth"])
async def obtain_access_token(credentials: CredentialsSchema):
    user = await authenticate(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    await update_last_login(user.id)
    data = get_jwt_pair_from_user(user)
    return data


@login_router.post("/refresh", response_model=JWTPairToken, tags=["auth"])
async def refresh(token: RefreshJWTToken):
    refresh_token = token.refresh
    data = get_jwt_pair_with_userid_from_refresh_token(refresh_token=refresh_token)
    user_id = data.pop("user_id")
    if user_id:
        await update_last_login(user_id)
    return data

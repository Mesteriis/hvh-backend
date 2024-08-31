from applications.users.auth.schemas import CredentialsSchema, JWTPairToken, RefreshJWTToken
from applications.users.auth.utils.contrib import authenticate
from applications.users.auth.utils.jwt import get_jwt_pair_from_user, get_jwt_pair_with_userid_from_refresh_token
from fastapi import APIRouter, HTTPException

auth_router = APIRouter()


@auth_router.post("/access-token", response_model=JWTPairToken, tags=["auth"])
async def access_token(credentials: CredentialsSchema):
    user = await authenticate(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    data = get_jwt_pair_from_user(user)
    data["user_id"] = str(user.id)
    return data


@auth_router.post("/refresh", response_model=JWTPairToken, tags=["auth"])
async def refresh(token: RefreshJWTToken):
    refresh_token = token.refresh
    data = get_jwt_pair_with_userid_from_refresh_token(refresh_token=refresh_token)
    return data

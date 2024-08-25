from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from applications.users.auth.dataclasses import AccessToken, RefreshToken
from applications.users.models import UserModel
from core.config import settings
from fastapi import HTTPException
from jwt import InvalidAlgorithmError, InvalidTokenError
from pytz import utc

ALGORITHM = settings.jwt_algorithm
access_token_jwt_type = "access"  # noqa: S105
refresh_token_jwt_type = "refresh"  # noqa: S105


def create_access_token(*, data: dict, expires_delta: timedelta | None = None) -> AccessToken:
    to_encode = data.copy()
    now = datetime.now(tz=utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt_access_token_expire_minutes)

    to_encode.update({"iat": now, "exp": expire, "token_type": access_token_jwt_type})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

    token = AccessToken(encoded_jwt=encoded_jwt)
    token.set_exp_from_datetime(expire)
    token.set_iat_from_datetime(now)
    return token


def create_refresh_token(*, data: dict, expires_delta: timedelta | None = None) -> RefreshToken:
    to_encode = data.copy()
    now = datetime.now(tz=UTC)

    if expires_delta is not None:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt_refresh_token_expire_minutes)

    to_encode.update({"iat": now, "exp": expire, "token_type": refresh_token_jwt_type})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

    token = RefreshToken(encoded_jwt=encoded_jwt)
    token.set_exp_from_datetime(expire)
    token.set_iat_from_datetime(now)
    return token


def decode_jwt(token: str, _: bool = True) -> dict[str, Any]:
    """
    Performs a validation of the given token and returns its payload
    dictionary.

    Raises a `TokenBackendError` if the token is malformed, if its
    signature check fails, or if its 'exp' claim indicates it has expired.
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except InvalidAlgorithmError as ex:
        raise HTTPException(status_code=400, detail="Invalid algorithm specified") from ex
    except InvalidTokenError as ex:
        raise HTTPException(status_code=400, detail="Token is invalid or expired") from ex


def get_jwt_pair_from_user(user: UserModel) -> dict[str, Any]:
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.jwt_refresh_token_expire_minutes)

    access_token = create_access_token(data={"user_id": str(user.id)}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"user_id": str(user.id)}, expires_delta=refresh_token_expires)
    return {
        "access": access_token.encoded_jwt,
        "access_expiration_at": access_token.exp,
        "refresh": refresh_token.encoded_jwt,
        "refresh_expiration_at": refresh_token.exp,
    }


def get_jwt_pair_with_userid_from_refresh_token(refresh_token: str) -> dict[str, Any]:
    payload = decode_jwt(refresh_token)
    user_id = payload.get("user_id", None)
    if not user_id:
        raise HTTPException(status_code=400, detail="No user related with token.")

    token_type = payload.get("token_type", None)
    if not token_type or token_type != refresh_token_jwt_type:
        raise HTTPException(status_code=400, detail="Token type is invalid.")

    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.jwt_refresh_token_expire_minutes)

    access_token = create_access_token(data={"user_id": user_id}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"user_id": user_id}, expires_delta=refresh_token_expires)

    return {
        "access": access_token.encoded_jwt,
        "access_expiration_at": access_token.exp,
        "refresh": refresh_token.encoded_jwt,
        "refresh_expiration_at": refresh_token.exp,
        "user_id": user_id,
    }

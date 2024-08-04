from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_403_FORBIDDEN

from apps.users.auth.schemas import JWTTokenPayload, CredentialsSchema
from apps.users.auth.utils.jwt import ALGORITHM
from apps.users.auth.utils.password import verify_and_update_password
from apps.users.models import UserModel
from apps.users.selectors import UserSelector
from core.config import settings

PASSWORD_RESET_JWT_SUBJECT = "passwordreset"
EMAIL_CONFIRMATION_JWT_SUBJECT = "emailconfirmation"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/access-token")


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": PASSWORD_RESET_JWT_SUBJECT, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == PASSWORD_RESET_JWT_SUBJECT
        return decoded_token["email"]
    except InvalidTokenError:
        return None


async def authenticate(credentials: CredentialsSchema) -> UserModel | None:
    if credentials.email:
        user = await UserSelector.get_by_email(credentials.email)
    elif credentials.username:
        user = await UserSelector.get_by_username(credentials.username)
    else:
        return None

    if user is None:
        return None

    verified, updated_password_hash = verify_and_update_password(
        credentials.password, user.password_hash
    )

    if not verified:
        return None
        # Update password hash to a more robust one if needed
    if updated_password_hash is not None:
        user.password_hash = updated_password_hash
        await user.save(update_fields=("password_hash",))
    return user

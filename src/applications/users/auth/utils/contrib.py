from datetime import datetime, timedelta

import jwt
from applications.users.auth.schemas import CredentialsSchema
from applications.users.auth.utils.password import verify_and_update_password
from applications.users.models import UserModel
from applications.users.selectors import UserSelector
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pytz import utc

PASSWORD_RESET_JWT_SUBJECT = "passwordreset"  # noqa: S105
EMAIL_CONFIRMATION_JWT_SUBJECT = "emailconfirmation"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/access-token")


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.email_reset_token_expire_hours)
    now = datetime.now(tz=utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": PASSWORD_RESET_JWT_SUBJECT, "email": email},
        settings.secret_key,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return decoded_token["email"]
    except InvalidTokenError:
        return None


async def authenticate(credentials: CredentialsSchema) -> UserModel | None:
    if credentials.email:
        user = await UserSelector.get_by_email(credentials.email)
    else:
        return None

    if user is None:
        return None

    verified, updated_password_hash = verify_and_update_password(credentials.password, user.hashed_password)

    if not verified:
        return None
    if updated_password_hash is not None:
        user.hashed_password = updated_password_hash
        await user.save()
    return user

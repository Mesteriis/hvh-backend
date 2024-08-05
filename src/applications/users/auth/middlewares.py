import jwt
from core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel


def verify_token(token: BaseModel = Depends(HTTPBearer())):
    try:
        return jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Token is invalid.") from e

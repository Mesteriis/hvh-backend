import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from core.config import settings


def verify_token(token: BaseModel = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(
            token.credentials, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is invalid.")

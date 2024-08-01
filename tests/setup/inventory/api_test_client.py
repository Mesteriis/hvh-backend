from typing import Any

from fastapi import FastAPI
from fastapi_users.jwt import generate_jwt
from fastapi_users.manager import VERIFY_USER_TOKEN_AUDIENCE, BaseUserManager
from httpx import AsyncClient
from sqlalchemy.orm import Session

from apps.users.models import UserModel
from apps.users.service import SECRET, UserManager


class AsyncApiTestClient(AsyncClient):
    _app: FastAPI = None
    auth_user = None
    _db: Session

    def __init__(self, **kwargs):
        self._app = kwargs.get("app")
        super().__init__(**kwargs)

    def url_for(self, name: str, /, **path_params: Any) -> str:
        return self._app.url_path_for(name, **path_params)

    async def force_auth(self, user: UserModel):
        self.auth_user = user
        auth_url = self.url_for("auth:jwt.login")
        response = await self.post(auth_url, data={"username": user.email, "password": user.email})
        token = response.json()["access_token"]
        self.headers.update({"Authorization": f"Bearer {token}"})
        return user

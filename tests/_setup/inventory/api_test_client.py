from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

from apps.users.auth.utils.jwt import get_jwt_pair_from_user
from apps.users.models import UserModel



class AsyncApiTestClient(AsyncClient):
    _app: FastAPI = None
    auth_user = None
    _db: Session

    def __init__(self, **kwargs):
        self._app = kwargs.get("app")
        super().__init__(**kwargs)

    def url_for(self, name: str, /, **path_params: Any) -> str:
        return self._app.url_path_for(name, **path_params)

    async def force_auth(
            self,
            user: UserModel = None,
            email: str = None,
            is_superuser=False,
            is_active=True,
    ) -> UserModel:
        if user and email:
            raise ValueError("You can't provide both user and email")
        if email:
            self.auth_user = await UserModel.get(email=email)
        else:
            self.auth_user = user or await self._generate_user(
                is_superuser=is_superuser,
                is_active=is_active,
            )

        update_fields = []
        if self.auth_user.is_active != is_active:
            self.auth_user.is_active = is_active
            update_fields.append("is_active")

        if self.auth_user.is_superuser != is_superuser:
            self.auth_user.is_superuser = is_superuser
            update_fields.append("is_superuser")

        if update_fields:
            await self.auth_user.save(update_fields=update_fields)

        data = get_jwt_pair_from_user(self.auth_user)

        self.headers.update({"Authorization": f"Bearer {data['access']}"})
        return self.auth_user

    @staticmethod
    async def _generate_user(
            is_superuser=False, is_active=True, is_email_verified=True
    ) -> UserModel:
        from tests._setup.inventory.factories import UserModelFactory
        user = await UserModelFactory.create(
            is_active=is_active,
            is_email_verified=is_email_verified,
            is_superuser=is_superuser,
        )
        return user

__all__ = ["settings"]

from typing import Any

import decouple
from pydantic import AnyHttpUrl, BaseModel, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import EnvTypeEnum


class APIServer(BaseSettings):
    url: AnyHttpUrl
    description: str


class DatabaseConfig(BaseModel):
    autocommit: bool = False
    autoflush: bool = False


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore",
    )

    env: EnvTypeEnum = EnvTypeEnum.LOCAL
    debug: bool = True
    title: str = "Home Video hub"
    description: str = "Self host service for video download and streaming, add integration in Home Assistant"
    version: str = "0.1.1"

    root_path: str = ""

    openapi_url: str = "/openapi.json"
    docs_url: str = "/"
    redoc_url: str = "/redoc"

    swagger_ui_oauth2_redirect_url: str = "/docs/oauth2-redirect"

    db_uri: PostgresDsn = "postgres://postgres:postgres@db:5432/postgres"
    db_config: DatabaseConfig = DatabaseConfig()
    radis_uri: RedisDsn = "redis://redis:6379/0"

    tg_bot_token: str | None = None

    init_logger: bool = True

    cors_allowed_origins: list = [
        "http://localhost:63342",
    ] + decouple.config("CORS_ALLOWED_ORIGINS", default="", cast=str).split(",")
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    secret_key: str = Field(
        "95ddeae2c9d1db376882724c002bf86e17c92f7928aaa348c39d56d87873d1e2", description="openssl rand -hex 32"
    )

    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440  # 1 day
    jwt_refresh_token_expire_minutes: int = 10080  # 7 days

    id_account_verification: bool = False
    email_reset_token_expire_hours: int = 24

    def init_settings(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "root_path": self.root_path,
            "openapi_url": self.openapi_url,
            "docs_url": self.docs_url,
            "redoc_url": self.redoc_url,
            "swagger_ui_oauth2_redirect_url": self.swagger_ui_oauth2_redirect_url,
        }


settings = AppSettings()

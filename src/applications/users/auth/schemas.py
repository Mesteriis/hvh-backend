from uuid import UUID

from pydantic import UUID4, BaseModel


class CredentialsSchema(BaseModel):
    username: str | None | None = None
    email: str | None | None = None
    password: str


class JWTPairToken(BaseModel):
    access: str
    access_expiration_at: int
    refresh: str
    refresh_expiration_at: int
    user_id: UUID


class RefreshJWTToken(BaseModel):
    refresh: str


class JWTTokenData(BaseModel):
    username: str = None


class JWTTokenPayload(BaseModel):
    user_id: str | UUID4 = None



import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserStruct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    hashed_password: str | None = None
    last_login: datetime | None = None
    is_active: bool = True
    is_superuser: bool = False
    date_joined: datetime = Field(default_factory=datetime.now)


class UserInBaseStruct(UserStruct):
    id: uuid.UUID


class UserRegisterStruct(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str


class UserUpdateStruct(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

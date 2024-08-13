import uuid
from datetime import date, datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field, field_validator



class UserStruct(BaseModel):
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


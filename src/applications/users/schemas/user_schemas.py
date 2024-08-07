from datetime import date, datetime

from applications.users.mixins import PasswordValidatorMixin
from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field, field_validator
from settings.manager import settings


class BaseProperties(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={"id", "is_superuser", "is_active"},
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class BaseUser(BaseProperties):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    created_at: datetime | None


class BaseUserCreate(BaseProperties):
    first_name: str | None
    last_name: str | None
    email: EmailStr
    username: str | None = None
    password: str


class BaseUserRegister(PasswordValidatorMixin, BaseProperties):
    first_name: str | None = None
    last_name: str | None = None
    imei: str | None = None
    email: EmailStr
    username: str | None = None
    password: str
    password_confirmation: str
    otp_code: str = Field(
        ...,
        min_length=settings.OTP_NUMBER_OF_DIGITS,
        max_length=settings.OTP_NUMBER_OF_DIGITS,
    )


class BaseUserUpdate(BaseProperties):
    email: EmailStr | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | str | None = None

    @field_validator("birth_date")
    def validate_birth_date(cls, value):
        if value == "":
            return None
        return value


class BaseUserDB(BaseUser):
    id: int
    hashed_id: UUID4
    password_hash: str
    updated_at: datetime
    last_login: datetime | None

    model_config = ConfigDict(from_attributes=True)


class BaseUserOut(BaseUser):
    id: str | UUID4

    model_config = ConfigDict(from_attributes=True)


class BaseRetrieveUser(BaseProperties):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None
    username: str | None = None
    is_active: bool | None
    is_superuser: bool | None
    is_email_verified: bool | None
    created_at: datetime | None
    birth_date: datetime | None = None
    avatar: str | None = None

    @field_validator("avatar", mode="before")
    def avatar_validator(cls, v) -> str | None:
        if v:
            return v.path
        return None

    model_config = ConfigDict(from_attributes=True)

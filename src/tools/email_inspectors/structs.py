from typing import Any

from pydantic import BaseModel, ConfigDict, computed_field, model_validator
from validate_email import validate_email_or_fail


class EmailItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: str
    extra_info: dict[str, Any] = {}
    error: Exception | None = None

    @computed_field
    def is_valid(self) -> bool:
        if "is_valid" in self.extra_info:
            return self.extra_info.get("is_valid")
        return False

    @model_validator(mode="before")
    def check_email_format(cls, data) -> None:
        email = data.get("email", None)
        if email is None:
            raise ValueError("Email address is required")
        try:
            validate_email_or_fail(email_address=email, **cls._get_settings())
            data["extra_info"]["is_valid"] = True

        except Exception as e:
            data["error"] = e
            data["extra_info"]["error"] = str(e).replace("\n", " ")
            data["extra_info"]["is_valid"] = False
        return data

    @classmethod
    def _get_settings(cls) -> dict:
        from .settings import CheckEmailSettings

        return CheckEmailSettings().model_dump()

    def as_csv_string(self) -> str:
        return f"{self.email},{self.is_valid},{self.extra_info.get("error", "")}\n"


class EmailList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    emails: list[EmailItem]

    @computed_field
    def total(self) -> int:
        return len(self.emails)

    @computed_field
    def valid(self) -> int:
        return sum(1 for email in self.emails if email.is_valid)

    @computed_field
    def invalid(self) -> int:
        return sum(1 for email in self.emails if not email.is_valid)

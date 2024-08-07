from applications.users.mixins import PasswordValidatorMixin
from pydantic import BaseModel


class ResetPasswordSchema(PasswordValidatorMixin, BaseModel):
    password: str
    password_confirmation: str
    reset_token: str

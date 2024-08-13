from pydantic import BaseModel


class ResetPasswordSchema(BaseModel):
    password: str
    password_confirmation: str
    reset_token: str

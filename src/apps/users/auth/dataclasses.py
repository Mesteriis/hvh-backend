from dataclasses import dataclass, field
from datetime import datetime, timedelta

from core.config import settings


@dataclass
class AccessToken:
    encoded_jwt: str = field(default_factory=str)
    iat: int = field(default_factory=lambda: int(datetime.utcnow().timestamp()) * 1000)
    exp: int = field(
        default_factory=lambda: int(
            (
                datetime.utcnow()
                + timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
            ).timestamp()
        )
        * 1000
    )

    def __post_init__(self):
        if self.iat <= 0:
            raise ValueError(
                "iat must be a positive integer representing Unix timestamp."
            )
        if self.exp <= self.iat:
            raise ValueError("exp must be greater than iat.")

    def set_iat_from_datetime(self, iat_datetime: datetime):
        self.iat = int(iat_datetime.timestamp()) * 1000

    def set_exp_from_datetime(self, exp_datetime: datetime):
        self.exp = int(exp_datetime.timestamp()) * 1000


@dataclass
class RefreshToken:
    encoded_jwt: str = field(default_factory=str)
    iat: int = field(default_factory=lambda: int(datetime.utcnow().timestamp()) * 1000)
    exp: int = field(
        default_factory=lambda: int(
            (
                datetime.utcnow()
                + timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
            ).timestamp()
        )
        * 1000
    )

    def __post_init__(self):
        if self.iat <= 0:
            raise ValueError(
                "iat must be a positive integer representing Unix timestamp."
            )
        if self.exp <= self.iat:
            raise ValueError("exp must be greater than iat.")

    def set_iat_from_datetime(self, iat_datetime: datetime):
        self.iat = int(iat_datetime.timestamp() * 1000)

    def set_exp_from_datetime(self, exp_datetime: datetime):
        self.exp = int(exp_datetime.timestamp() * 1000)

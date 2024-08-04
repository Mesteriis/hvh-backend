from datetime import datetime

import pyotp
from settings.manager import settings
from tortoise import timezone


def generate_otp_code_with_secret() -> tuple[str, str]:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(
        secret,
        digits=settings.OTP_NUMBER_OF_DIGITS,
        interval=settings.OTP_EXPIRATION_INTERVAL,
    )
    return totp.now(), secret


def verify_otp_code(otp_code: str, secret: str) -> bool:
    totp = pyotp.TOTP(
        secret,
        digits=settings.OTP_NUMBER_OF_DIGITS,
        interval=settings.OTP_EXPIRATION_INTERVAL,
    )
    return totp.verify(otp_code, valid_window=1)


def calculate_remaining_time(expiration_at: datetime) -> int:
    time_diff = expiration_at - timezone.now()
    seconds_remaining = time_diff.total_seconds()
    return int(seconds_remaining)

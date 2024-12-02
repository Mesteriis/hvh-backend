from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import SMTP_HELO_HOST, SMTP_FROM_ADDRESS


class CheckEmailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='CHECK_EMAIL_',
    )
    check_format: bool = True
    check_blacklist: bool = True
    check_dns: bool = True
    dns_timeout: float = 10
    check_smtp: bool = True
    smtp_timeout: float = 10
    smtp_helo_host: str = SMTP_HELO_HOST
    smtp_from_address: str = SMTP_FROM_ADDRESS
    smtp_skip_tls: bool = False
    smtp_debug: bool = False

__all__ = ["get_settings"]

from config import settings


def get_settings() -> settings.AppSettings:
    return settings.AppSettings()

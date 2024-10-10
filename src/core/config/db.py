from __future__ import annotations

from tortoise import Model

from tools.class_finder import ClassFinder
from core.config import settings

def get_app_list():
    from contants import APP_FOLDER
    return ClassFinder(APP_FOLDER, Model).build_tortoise_imports()

def get_tortoise_config() -> dict:
    app_list = get_app_list()
    app_list.append("aerich.models")
    config = {
        "connections": settings.db_uri,
        "apps": {
            "models": {
                "models": app_list,
                "default_connection": "default",
                "schema": "public",
                "use_tz": True,
                "timezone": "UTC",

            },
            "signals": ["aerich.signals"],
        },
    }
    return config

TORTOISE_ORM = get_tortoise_config()


def get_uri() -> str:
    from core.config import settings

    return str(settings.db_uri)



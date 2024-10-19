from __future__ import annotations

from tools.class_finder import ClassFinder
from tortoise import Model


def get_uri() -> str:
    from core.config import settings

    return str(settings.db_uri)


def get_app_list():
    from contants import APP_FOLDER

    return ClassFinder(APP_FOLDER, Model).build_tortoise_imports()


def get_tortoise_config() -> dict:
    app_list = get_app_list()
    app_list.append("aerich.models")
    config = {
        "connections": get_uri(),
        "apps": {
            "models": {
                "models": app_list,
            },
            "signals": ["aerich.signals"],
        },
    }
    return config


TORTOISE_ORM = get_tortoise_config()


async def init_db():
    from tortoise import Tortoise

    await Tortoise.init(
        db_url=get_uri(),
        modules={"models": get_app_list()},
    )
    await Tortoise.generate_schemas()

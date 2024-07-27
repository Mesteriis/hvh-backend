import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from tools.class_finder import ClassFinder

config = context.config

ROOT_PATH = Path(__file__).parent.parent.resolve()
APP_PATH = ROOT_PATH / "src"
TEST_PATH = ROOT_PATH / "tests"
sys.path.append(str(APP_PATH.absolute()))
sys.path.append(str(TEST_PATH.absolute()))

from config.db import Base, settings  # noqa

db_url = os.environ.get(
    "DATABASE_URL",
    str(settings.db_uri)
)

config.set_main_option(
    "sqlalchemy.url",
    db_url
)
fileConfig(config.config_file_name)

target_metadata = Base.metadata
cf = ClassFinder(APP_PATH, Base)
cf.run()
print(f"db_url: {db_url}")  # noqa


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        future=True
    )

    async def async_main():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(async_main())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

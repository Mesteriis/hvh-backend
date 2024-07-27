import os
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

config = context.config

# ROOT_PATH = Path(__file__).parent.parent.resolve()
# APP_PATH = ROOT_PATH / "src"
# TEST_PATH = ROOT_PATH / "tests"
# sys.path.append(str(APP_PATH.absolute()))
# sys.path.append(str(TEST_PATH.absolute()))

from config.db import Base, settings  # noqa
from apps.users.models import User  # noqa

db_url = os.environ.get(
    "DATABASE_URL",
    str(settings.db_uri)
)
print(f"db_url: {db_url}")  # noqa
config.set_main_option(
    "sqlalchemy.url",
    db_url
)
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


async def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())

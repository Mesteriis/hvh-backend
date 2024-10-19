import asyncio
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from contants import ROOT_DIR, APP_FOLDER
from core.config import settings

# TODO.md: Move to setup fixture
settings.db_uri = str(settings.db_uri) + '_test'
DATABASE_URL = settings.db_uri
settings.init_logger = False

from core.init_app import App  # noqa
from tests.inventory import drop_database, create_database  # noqa
from tests.inventory import AsyncApiTestClient  # noqa
from tests.inventory import set_level_logging  # noqa
from tests.settings import pytest_settings  # noqa

pytest_plugins = pytest_settings.pytest_plugins
set_level_logging(pytest_settings.logger_level)

engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(  # type: ignore
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope='session')
async def setup_test_database():
    await drop_database(DATABASE_URL)
    await create_database(DATABASE_URL)
    yield
    if pytest_settings.clean_db:
        await drop_database(DATABASE_URL)


# @pytest.fixture(scope='session')
# async def event_loop():
#     policy = asyncio.get_event_loop_policy()
#     try:
#         loop = policy.get_event_loop()
#     except RuntimeError:
#         loop = policy.new_event_loop()
#     try:
#         yield loop
#     finally:
#         loop.close()


@pytest.fixture(scope='session')
def alembic_config(setup_test_database):
    alembic_cfg = Config(str(ROOT_DIR / 'alembic.ini'))
    alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
    alembic_cfg.set_main_option('prepend_sys_path', str(APP_FOLDER))
    alembic_cfg.set_main_option('script_location', str(ROOT_DIR / 'migrations'))
    return alembic_cfg


@pytest.fixture(scope='session')
def alembic_engine(alembic_config):
    return engine.sync_engine


@pytest.fixture(scope='session', autouse=True)
def apply_migrations(alembic_config):
    command.upgrade(alembic_config, 'head')


@pytest.fixture(scope='session')
async def async_engine(apply_migrations):
    yield engine


@pytest.fixture(scope='session', autouse=True)
async def session(async_engine):
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()
        await session.close()


@pytest.fixture(scope='session')
async def client():
    from main import app
    async with AsyncApiTestClient(app=app, base_url='http://test') as client:
        yield client

@pytest.fixture(scope="module")
def event_loop(client: AsyncApiTestClient) -> Generator:
    yield client.task.get_loop()

# b-case fixtures
@pytest.fixture()
def yt_url_video():
    return "https://www.youtube.com/watch?v=2WZ5mN_tcAg"


@pytest.fixture()
def yt_url_playlist():
    return "https://www.youtube.com/playlist?list=PLySj34Zkq0TAdQTPMeGTGZafX-kqgoYbT"


@pytest.fixture()
def yt_url_channel():
    return "https://www.youtube.com/channel/UChJ4IOQrs63Y5_Rx5aqolZw"

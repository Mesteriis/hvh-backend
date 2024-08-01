import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.db import get_session
from config.settings import settings
from contants import ROOT_DIR, APP_FOLDER
from core.init_app import App
from tests.settings import pytest_settings
from tests.setup.db_tools import drop_database, create_database
from tests.setup.inventory.api_test_client import AsyncApiTestClient
from tests.setup.inventory.logging import set_level_logging

settings.db_uri = str(settings.db_uri) + '_test'
DATABASE_URL = settings.db_uri
settings.init_logger = False

set_level_logging(pytest_settings.logger_level)

engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(  # type: ignore
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope='function', autouse=True)
def init_test_session(mocker):
    mocker.patch.object(App, 'init_logger', side_effect=None)


@pytest.fixture(scope='session')
async def setup_test_database():
    await drop_database(DATABASE_URL)
    await create_database(DATABASE_URL)
    yield
    if pytest_settings.clean_db:
        await drop_database(DATABASE_URL)


@pytest.fixture(scope='session')
def alembic_config(setup_test_database):
    alembic_cfg = Config(str(ROOT_DIR.parent / 'alembic.ini'))
    alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
    alembic_cfg.set_main_option('prepend_sys_path', str(APP_FOLDER))
    alembic_cfg.set_main_option('script_location', str(ROOT_DIR.parent / 'migrations'))
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


@pytest.fixture(scope='function', autouse=True)
async def session(async_engine):
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope='session')
async def client():
    from main import app

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncApiTestClient(app=app, base_url='http://test') as client:
        yield client

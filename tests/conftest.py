# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport
from tortoise.contrib.test import MEMORY_SQLITE

from tests.inventory.api_test_client import AsyncApiTestClient
from core.config import settings
from .inventory.factories import *


settings.db_uri = MEMORY_SQLITE
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
try:
    from main import app
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    logger.error(f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n")
    raise



@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kw) -> AsyncGenerator[AsyncApiTestClient, None]:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncApiTestClient(transport=transport, base_url=base_url, **kw) as c:
            yield c


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncApiTestClient, None]:
    async with client_manager(app, "http://test") as c:
        yield c




import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api import api_router
from api.v1.sse_views import dashboard_streams
from contants import STATIC_FOLDER
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tools.async_to_sync import run_coroutine_sync
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise

from .async_logger import DEFAULT_LOGGERS, HandlerItem, init_logger
from .async_logger.handlers import PrintLog
from .config.db import get_models_paths
from .exceptions import APIException, on_api_exception, validation_exception_handler

logger = logging.getLogger(__name__)


class App(FastAPI):
    __settings: "AppSettings"  # noqa: F821

    def __init__(self):
        self.__settings = self.get_settings()
        super().__init__(**self.__settings.init_settings())
        # if self.__settings.init_logger:
        #     self.init_logger()
        self.connect_db()
        self.register_routers()
        self.register_exceptions()
        self.register_middlewares()
        self.mount_static()

    @staticmethod
    def get_settings() -> "AppSettings":  # noqa: F821
        from core.config import settings

        return settings

    def register_routers(self):
        @self.get("/healthcheck", tags=["healthcheck"])
        def healthcheck():
            return {"status": "ok"}

        self.include_router(self.ssr_router)

        self.include_router(api_router)

    @property
    def ssr_router(self):
        root_router = APIRouter(prefix="/ssr", tags=["ssr"])
        root_router.get("/sse_dashboard")(dashboard_streams)
        return root_router

    def register_exceptions(self):
        self.add_exception_handler(APIException, on_api_exception)  # noqa: type
        self.add_exception_handler(RequestValidationError, validation_exception_handler)  # noqa: type

    def register_middlewares(self):
        self.add_middleware(
            CORSMiddleware,  # noqa: type
            allow_origins=self.__settings.cors_allowed_origins,
            allow_credentials=self.__settings.cors_allow_credentials,
            allow_methods=self.__settings.cors_allow_methods,
            allow_headers=self.__settings.cors_allow_headers,
        )

    def init_logger(self):
        handlers = [
            HandlerItem(func=PrintLog()),
        ]
        for el in DEFAULT_LOGGERS:
            el.handlers = handlers
        init_logger(self, handlers=handlers, loggers=DEFAULT_LOGGERS)
        msg = f"Настройки: {self.__settings.model_dump_json(indent=2)}"
        logger.debug(msg)

    def mount_static(self):
        self.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

    def connect_db(self):
        async def awrapper():
            await Tortoise.init(db_url=str(self.__settings.db_uri), modules={"models": get_models_paths()})
            await Tortoise.generate_schemas()

        run_coroutine_sync(awrapper())

    @staticmethod
    @asynccontextmanager
    async def lifespan_test(app: FastAPI) -> AsyncGenerator[None, None]:
        config = generate_config(
            App.get_settings().db_uri,
            app_modules={"models": ["models"]},
            testing=True,
            connection_label="models",
        )
        async with RegisterTortoise(
            app=app,
            config=config,
            generate_schemas=True,
            add_exception_handlers=True,
            _create_db=True,
        ):
            # db connected
            yield
            # app teardown
        # db connections closed
        await Tortoise._drop_databases()

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        if getattr(app.state, "testing", None):
            async with App.lifespan_test(app) as _:
                yield
        else:
            # app startup
            async with App.register_orm(app):
                # db connected
                yield
                # app teardown
            # db connections closed

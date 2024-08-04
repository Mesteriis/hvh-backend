import logging

from api import api_router
from core.config import AppSettings
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

from .async_logger import DEFAULT_LOGGERS, HandlerItem, init_logger
from .async_logger.handlers import PrintLog
from .exceptions import APIException, integrity_error_handler, on_api_exception, validation_exception_handler

logger = logging.getLogger(__name__)


class App(FastAPI):
    __settings: AppSettings

    def __init__(self):
        self.__settings = self.get_settings()
        super().__init__(**self.__settings.init_settings())
        if self.__settings.init_logger:
            self.init_logger()
        self.register_routers()
        self.register_exceptions()
        self.register_middlewares()

    @staticmethod
    def get_settings() -> AppSettings:
        from core.config import settings
        return settings

    def register_routers(self):
        @self.get("/healthcheck", tags=["healthcheck"])
        def healthcheck():
            return {"status": "ok"}

        self.include_router(api_router)

    def register_exceptions(self):
        self.add_exception_handler(APIException, on_api_exception)  # noqa: type
        self.add_exception_handler(RequestValidationError, validation_exception_handler)  # noqa: type
        self.add_exception_handler(IntegrityError, integrity_error_handler)  # noqa: type

    def register_middlewares(self):
        self.add_middleware(
            CORSMiddleware,  # noqa: type
            allow_origins=self.__settings.cors_allowed_origins,
            allow_credentials=self.__settings.cors_allow_credentials,
            allow_methods=self.__settings.cors_allow_methods,
            allow_headers=self.__settings.cors_allow_headers,
            expose_headers=["X-Request-ID"],
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

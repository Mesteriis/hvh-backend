from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

from .exceptions import integrity_error_handler, APIException, on_api_exception, validation_exception_handler


class App(FastAPI):
    def __init__(self):
        self.settings = self.get_settings()
        super().__init__(**self.settings.init_settings())
        self.register_routers()
        self.register_exceptions()
        self.register_middlewares()

    @classmethod
    def get_settings(cls):
        from config import settings
        return settings.AppSettings()

    def register_routers(self):
        @self.get("/healthcheck")
        def healthcheck():
            return {"status": "ok"}

    def register_exceptions(self):
        self.add_exception_handler(APIException, on_api_exception)  # noqa: type
        self.add_exception_handler(RequestValidationError, validation_exception_handler)  # noqa: type
        self.add_exception_handler(IntegrityError, integrity_error_handler)  # noqa: type

    def register_middlewares(self):
        self.add_middleware(CorrelationIdMiddleware)  # noqa: type
        self.add_middleware(
            CORSMiddleware,  # noqa: type
            allow_origins=self.settings.cors_allowed_origins,
            allow_credentials=self.settings.cors_allow_credentials,
            allow_methods=self.settings.cors_allow_methods,
            allow_headers=self.settings.cors_allow_headers,
            expose_headers=['X-Request-ID'],
        )

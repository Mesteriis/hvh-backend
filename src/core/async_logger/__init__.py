__all__ = [
    "init_logger",
    "HandlerItem",
    "LoggersItem",
    "LoggerSettings",
    "DEFAULT_LOGGERS",
]

import logging
from logging.config import dictConfig

from fastapi import FastAPI

from .config import (
    HandlerItem,
    LoggersItem,
    DEFAULT_HANDLERS,
    DEFAULT_LOGGERS,
    json_formatter,
    LoggerSettings,
)
from .middlewares import LoggingMiddleware, CorrelationIdMiddleware

logger = logging.getLogger(__name__)


def init_logger(
    app: FastAPI,
    handlers: list[HandlerItem] = DEFAULT_HANDLERS,
    loggers: list[LoggersItem] = DEFAULT_LOGGERS,
) -> None:
    """
    Инициализирует логгер для данного приложения FastAPI.

    :param FastAPI app: Приложение FastAPI, которое требует логгирования.
    :param list[HandlerItem] handlers: Список обработчиков, которые будет использовать логгер.
                                       Если не указано, будут использованы обработчики по умолчанию.
    :param list[LoggersItem] loggers: Список логгеров для настройки. Если не указаны, будут использованы логгеры по умолчанию.
    :return: None
    """

    try:
        settings = LoggerSettings.model_validate(
            {
                "handlers": handlers,
                "formatters": [
                    json_formatter,
                ],
                "loggers": loggers,
            },
        )
    except Exception as e:
        logger.error(f"Ошибка журнала настроек инициализации: {e}")
        logger.info("Инициализирован асинхронный logger настроек по умолчанию")
    else:
        try:
            data_settings = settings.convert_to_log_settings()
            dictConfig(data_settings)
            app.middleware("http")(LoggingMiddleware())
        except Exception as e:
            logger.error(f"Ошибка инициализации асинхронного logger: {e}")
            logger.info("Инициализировать logger по умолчанию")
            settings = LoggerSettings.model_validate(
                {
                    "handlers": DEFAULT_HANDLERS,
                    "loggers": DEFAULT_LOGGERS,
                },
            )
            dictConfig(settings.convert_to_log_settings())
    finally:
        app.add_middleware(CorrelationIdMiddleware) # noqa: type

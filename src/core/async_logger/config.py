from logging import Handler, Formatter
from typing import Callable

from pydantic import BaseModel, model_validator, ConfigDict

from .dispatcher import AsyncLogDispatcher
from .formatter import JSONLogFormatter
from .handlers import PrintLog
from .structures.base import LogMessage
from .tools import get_import_str_from_obj


class BaseModelConfig(BaseModel):
    """
    Наследуется от базового класса BaseModel и содержит одно поле "model_config"
    позволяющее добавлять произвольные типы данных.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)


class FormatterItem(BaseModelConfig):
    """
    Представляющий элемент форматтера. Он наследуется от BaseModelConfig и
    содержит информацию о классе форматтера, а также используемую aria.
    """

    klass: type[Formatter] = JSONLogFormatter
    aria: str = "()"

    def to_logger_settings_item(self):
        return {
            self.klass.__name__: {
                self.aria: get_import_str_from_obj(JSONLogFormatter),
            },
        }


json_formatter = FormatterItem(klass=JSONLogFormatter)


class HandlerItem(BaseModelConfig):
    """
    Представляет элемент обработчика. Он определяет форматтер для использования,
    класс обработчика для применения и функцию для вызова при обработке записи.
    """

    formatter: FormatterItem = json_formatter
    klass: type[Handler] = AsyncLogDispatcher
    func: Callable[[LogMessage], None]

    def to_logger_settings_item(self):
        data = {
            self.func.name: {
                "formatter": self.formatter.klass.__name__,
                "class": get_import_str_from_obj(self.klass),
                "func": self.func,
            },
        }
        return data


class LoggersItem(BaseModelConfig):
    """
    Определяет настройки для логгера. Он может быть использован для настройки разных аспектов логгера,
    таких как уровень дебага, версия, отключение существующих логгеров, форматтеры, обработчики и логгеры.
    """

    name: str
    handlers: list[HandlerItem]
    level: str
    propagate: bool

    def to_logger_settings_item(self):
        data = {
            self.name: {
                "level": self.level,
                "propagate": self.propagate,
                "handlers": [el.func.name for el in self.handlers],
            },
        }
        return data


class LoggerSettings(BaseModelConfig):
    """
    Обеспечивает настройку логгера, включая уровень дебага,
    версию, отключение существующих логгеров, форматтеры, обработчики и логгеры.
    """

    debug: bool = True
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: list[FormatterItem] = [json_formatter]
    handlers: list[HandlerItem]
    loggers: list[LoggersItem]

    @model_validator(mode="before")
    def check_relation_handler_and_formatter(cls, v):
        # formatters = [item for item in v['formatters']]
        # for handler in v.handlers:
        #     if handler.formatter.name not in formatters:
        #         raise ValidationError(f"Formatter {handler.formatter} not found in formatters")
        return v

    def convert_to_log_settings(self):
        data = {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": {},
            "handlers": {},
            "loggers": {},
        }
        for formatter in self.formatters:
            data["formatters"].update(formatter.to_logger_settings_item())
        for handler in self.handlers:
            data["handlers"].update(handler.to_logger_settings_item())
        for logger in self.loggers:
            data["loggers"].update(logger.to_logger_settings_item())

        return data


_handler_print_log = HandlerItem(func=PrintLog())

DEFAULT_HANDLERS = [_handler_print_log]

DEFAULT_LOGGERS = [
    LoggersItem(
        name="",
        handlers=DEFAULT_HANDLERS,
        level="DEBUG",
        propagate=False,
    ),
    LoggersItem(
        name="uvicorn",
        handlers=DEFAULT_HANDLERS,
        level="INFO",
        propagate=False,
    ),
    LoggersItem(
        name="uvicorn.access",
        handlers=DEFAULT_HANDLERS,
        level="ERROR",
        propagate=False,
    ),
]

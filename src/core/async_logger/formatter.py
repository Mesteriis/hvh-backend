import datetime
import logging
import traceback

from .abstract import ABCFormatter
from .constants import NAMED_LOG_LEVEL
from .structures.base import LogMessage, BaseJsonLogSchema


class JSONLogFormatter(ABCFormatter, logging.Formatter):
    """
    Кастомизированный класс-форматер для логов в формате json
    """

    __default_kwargs = ["fmt", "datefmt", "style", "validate"]
    __extra_kwargs = {}

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__default_kwargs:
                self.__extra_kwargs[k] = v
                del kwargs[k]
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord, *args, **kwargs) -> LogMessage:
        """
        Преобразование объекта в LogMessage

        :param record: объект журнала
        :return: log dict
        """
        return LogMessage(**self._format_log_object(record))

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        """
        Перевод записи лога в json формат с необходимым перечнем полей

        :param record: Объект журнала.
        :return: Словарь с объектами журнала.
        """

        now = (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        message = record.getMessage()
        duration = record.duration if hasattr(record, "duration") else record.msecs
        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level=record.levelno,
            level_name=NAMED_LOG_LEVEL[record.levelno],
            message=message,
            source=record.name,
            duration=duration,
            app_name="settings.SOFT_NAME",
            app_version="settings.project_version",
            app_env="settings.env",
        )

        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = traceback.format_exception(*record.exc_info)

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        json_log_object = json_log_fields.model_dump(exclude_unset=True, by_alias=True)

        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)

        return json_log_object

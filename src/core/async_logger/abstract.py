from abc import ABC, abstractmethod
from logging import LogRecord


class ABCConverter(ABC):
    """Абстрактный класс конвертера."""

    @abstractmethod
    def convert(self) -> dict:
        """Преобразование записи в строку."""


class ABCHandler(ABC):
    """Абстрактный класс для обработчика."""

    @abstractmethod
    def __call__(self, msg):
        """Call handler."""


class ABCFormatter(ABC):
    """Абстрактный класс для обработчика."""

    @abstractmethod
    def format(self, record: LogRecord, *args, **kwargs):
        """Обработчик вызова."""

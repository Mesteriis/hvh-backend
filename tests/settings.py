import logging
from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import DB_URI_IN_MEMORY, DB_URI_FILE, DB_URI_POSTGRES
from .constants import TEST_MEDIA_FOLDER
from tests.inventory.logging import set_level_logging


class DataBaseTypeInTestEnum(str, Enum):
    in_memory = "in_memory"
    file = "file"
    postgres = "postgres"


class PyTestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PYTEST_", extra="ignore")

    db_type: DataBaseTypeInTestEnum = DataBaseTypeInTestEnum.postgres

    pytest_plugins: list[str] = [
        "tests.inventory.factories",
    ]
    logger_level: str = "ERROR"
    logger_name: str = "tests"

    other_logging_level: str = "ERROR"
    test_server_base_url: str = "http://test"

    @property
    def db_uri(self):
        match self.db_type:
            case DataBaseTypeInTestEnum.in_memory:
                return DB_URI_IN_MEMORY
            case DataBaseTypeInTestEnum.file:
                return DB_URI_FILE
            case DataBaseTypeInTestEnum.postgres:
                return DB_URI_POSTGRES
            case _:
                return DB_URI_IN_MEMORY

    clean_media_folder: bool = True
    clean_db: bool = False
    test_backend: str = "asyncio"

    test_media_folder: Path = TEST_MEDIA_FOLDER

    _logger: logging.Logger | None = None

    @property
    def logger(self) -> logging.Logger:
        if not self._logger:
            set_level_logging(pytest_settings.other_logging_level)
            self._logger = logging.getLogger(self.logger_name)
        self._logger.setLevel(self.logger_level)
        return self._logger

    def print(self):
        self.logger.info("Test environment is set up:")
        lines = [f"- {k}: {v}" for k, v in self.model_dump().items()]
        lines.append(f"- DB_URI: {self.db_uri}")
        self.logger.info("\n".join(lines))


pytest_settings = PyTestSettings()

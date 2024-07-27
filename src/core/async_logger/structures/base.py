from datetime import datetime

from pydantic import BaseModel


class BaseJsonLogSchema(BaseModel):
    """
    Схема основного тела лога в формате JSON
    """

    thread: int | str
    level: int
    level_name: str
    message: str
    source: str
    timestamp: str
    app_name: str
    app_version: str
    app_env: str
    duration: int | float
    exceptions: list[str] | None = None
    trace_id: str | None = None
    span_id: str | None = None
    parent_id: str | None = None

    class Config:
        populate_by_name = True


class LogMessage(BaseModel):
    """
    Модель структурированного ведения журналов логов.

    Она содержит поля для метаданных, таких как отметка времени, уровень журнала,
    идентификатор потока и т. д., а также подробности запроса и ответа.
    """

    app_env: str
    app_name: str
    app_version: str
    duration: int | float
    exceptions: list = None
    level_name: str
    level: int
    message: str
    remote_ip: str = None
    remote_port: int = None
    request_body: str = None
    request_content_type: str = None
    request_direction: str = None
    request_headers: dict = {}
    request_host: str = None
    request_method: str = None
    request_path: str = None
    request_protocol: str = None
    request_referer: str = None
    request_size: int = None
    request_uri: str = None
    response_body: str | bytes = None
    response_headers: str = None
    response_size: int = None
    response_status_code: int = None
    source: str
    timestamp: datetime
    thread: int | str
    trace_id: str | None = None
    span_id: str | None = None
    parent_id: str | None = None

from datetime import datetime
from typing import Union

from pydantic import BaseModel


class BaseJsonLogSchema(BaseModel):
    """
    Схема основного тела лога в формате JSON
    """

    thread: Union[int, str]
    level: int
    level_name: str
    message: str
    source: str
    timestamp: str
    app_name: str
    app_version: str
    app_env: str
    duration: Union[int, float]
    exceptions: Union[list[str], None] = None
    trace_id: Union[str, None] = None
    span_id: Union[str, None] = None
    parent_id: Union[str, None] = None

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
    duration: Union[int, float]
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
    response_body: Union[str, bytes] = None
    response_headers: str = None
    response_size: int = None
    response_status_code: int = None
    source: str
    timestamp: datetime
    thread: Union[int, str]
    trace_id: Union[str, None] = None
    span_id: Union[str, None] = None
    parent_id: Union[str, None] = None

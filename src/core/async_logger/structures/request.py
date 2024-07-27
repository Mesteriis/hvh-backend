from pydantic import BaseModel


class RequestJsonLogSchema(BaseModel):
    """
    Схема части запросов-ответов лога в формате JSON
    """

    request_uri: str = None
    request_referer: str = None
    request_protocol: str = None
    request_method: str = None
    request_path: str = None
    request_host: str = None
    request_size: int
    request_content_type: str = None
    request_headers: dict = None
    request_body: str = None
    request_direction: int | str = None
    remote_ip: str = None
    remote_port: int = None
    response_status_code: int
    response_size: int
    response_headers: str = None
    response_body: str | bytes = None
    duration: int | float

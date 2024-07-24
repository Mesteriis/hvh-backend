import http
import json
import math
import time
from logging import getLogger

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message

from ..structures.request import RequestJsonLogSchema

EMPTY_VALUE = ""
logger = getLogger("request")


class LoggingMiddleware:
    """
    Обеспечивает функцию ведения журнала запросов и ответов на HTTP-сервере.

    :methods get_protocol: принимает объект Request, возвращает протокол запроса.
    :methods set_body: принимает объект Request и объект bytes, устанавливает тело запроса данного объекта bytes.
    :methods get_body: принимает объект Request, возвращает тело запроса в виде bytes и устанавливает тело запроса.
    :methods __call__: принимает различные аргументы, включая объект Request и функцию call_next,
                       реализует логику ведения запросов и ответов, возвращает ответ.
    """

    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return EMPTY_VALUE

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Message:
            return {"type": "http.request", "body": body}

        request._receive = receive

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def __call__(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        *args,
        **kwargs,
    ):
        start_time = time.time()
        exception_object = None
        # Request Side
        try:
            raw_request_body = await request.body()
            await self.set_body(request, raw_request_body)
            raw_request_body = await self.get_body(request)
            request_body = raw_request_body.decode()
        except Exception:  # noqa
            request_body = EMPTY_VALUE

        server: tuple = request.get("server", ("localhost", "8000"))
        request_headers: dict = dict(request.headers.items())
        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:  # noqa: B902
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        duration: int = math.ceil((time.time() - start_time) * 1000)
        try:
            body = response_body.decode("utf-8")
        except UnicodeDecodeError:
            body = response_body
        request_json_fields = RequestJsonLogSchema(
            request_uri=str(request.url),
            request_referer=request_headers.get("referer", EMPTY_VALUE),
            request_protocol=await self.get_protocol(request),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f"{server[0]}:{server[1]}",
            request_size=int(request_headers.get("content-length", 0)),
            request_content_type=request_headers.get("content-type", EMPTY_VALUE),
            request_headers=request_headers,
            request_body=request_body,
            request_direction="in",
            remote_ip=request.client[0],
            remote_port=request.client[1],
            response_status_code=response.status_code,
            response_size=int(response_headers.get("content-length", 0)),
            response_headers=json.dumps(response_headers),
            response_body=body,
            duration=duration,
        ).model_dump(exclude_unset=True, by_alias=True)

        message = (
            f'{"Ошибка" if exception_object else "Ответ"} '
            f"с кодом {response.status_code} "
            f'на запрос {request.method} "{str(request.url)}", '
            f"за {duration} мс"
        )
        logger.info(
            message,
            extra={"request_json_fields": request_json_fields, "to_mask": True},
            exc_info=exception_object,
        )
        return response

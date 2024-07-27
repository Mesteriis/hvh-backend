import logging
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from starlette.datastructures import MutableHeaders

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("asgi_correlation_id")

correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def is_valid_uuid4(uuid_: str) -> bool:
    """
    Проверьте, является ли строка допустимым uuid v4.
    """
    try:
        return bool(UUID(uuid_, version=4))
    except ValueError:
        return False


FAILED_VALIDATION_MESSAGE = "значение заголовка запроса не прошло проверку (%s),"


@dataclass
class CorrelationIdMiddleware:
    app: "ASGIApp"
    header_name: str = "X-Request-ID"
    update_request_header: bool = True

    generator: Callable[[], str] = field(default=lambda: uuid4().hex)
    validator: Callable[[str], bool] | None = field(default=is_valid_uuid4)
    transformer: Callable[[str], str] | None = field(default=lambda a: a)

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        headers = MutableHeaders(scope=scope)
        header_value = headers.get(self.header_name.lower())

        validation_failed = False
        if not header_value:
            id_value = self.generator()
        elif self.validator and not self.validator(header_value):
            validation_failed = True
            id_value = self.generator()
        else:
            id_value = header_value

        if self.transformer:
            id_value = self.transformer(id_value)

        if validation_failed is True:
            logger.warning(FAILED_VALIDATION_MESSAGE, id_value)

        if id_value != header_value and self.update_request_header is True:
            headers[self.header_name] = id_value

        correlation_id.set(id_value)

        async def handle_outgoing_request(message: "Message") -> None:
            if message["type"] == "http.response.start" and correlation_id.get():
                headers = MutableHeaders(scope=message)
                headers.append(self.header_name, correlation_id.get())

            await send(message)

        await self.app(scope, receive, handle_outgoing_request)
        return

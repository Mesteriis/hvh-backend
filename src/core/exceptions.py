import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY

logger = logging.getLogger(__name__)


class LoggingError(Exception):
    def __init__(self, message: str, *_, **kwargs):
        self.message = message
        logger.exception(message, extra=kwargs)
        super().__init__(message)


class SettingNotFound(Exception):
    pass


class APIException(Exception):
    def __init__(self, error_code: int = 000, status_code: int = 500, detail="", message="", *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        self.error_code = error_code
        self.message = message
        self.detail = detail
        self.status_code = status_code

    def __str__(self):
        return f"APIException(status_code={self.status_code}, detail={self.message})"


async def on_api_exception(_: Request, exception: APIException) -> JSONResponse:
    content = {"errors": {"error_code": exception.error_code}}

    if exception.message:
        content["errors"]["message"] = exception.message

    if exception.detail:
        content["errors"]["detail"] = exception.detail

    return JSONResponse(content=content, status_code=exception.status_code)


# TODO.md: uncomment when android team is ready to accept extended json (rn they only want description -_-)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    details = exc.errors()
    errors_with_descriptions = []

    for error in details:
        errors_with_descriptions.append(f'{"".join(str(er) for er in error["loc"])} — {error["msg"]}')

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": ", ".join(errors_with_descriptions)}),
    )


async def integrity_error_handler(_: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=HTTP_409_CONFLICT,
        content=jsonable_encoder({"detail": f"{exc}"}),
    )

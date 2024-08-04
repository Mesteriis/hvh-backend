import logging

from applications.auth.schemas import MsgSchema
from applications.users.interactors import PasswordInteractor
from applications.users.schemas import ResetPasswordSchema
from fastapi import APIRouter
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
password_api_router = APIRouter()


@password_api_router.post("/password-recovery/{email}", status_code=204, tags=["users"])
async def recover_password(email: str):
    await PasswordInteractor().recover_password(email=email)
    return {}


@password_api_router.post("/reset-password/", status_code=200, tags=["users"], response_model=MsgSchema)
async def post_reset_password(payload: ResetPasswordSchema):
    await PasswordInteractor().reset_password(payload=payload)
    return JSONResponse(status_code=200, content={"message": "Password updated successfully"})

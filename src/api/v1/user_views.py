import logging
from dataclasses import asdict
from urllib.parse import urljoin

from applications.auth.models import OTPCode
from applications.auth.schemas import JWTPairToken
from applications.auth.utils import verify_otp_code
from applications.auth.utils.contrib import get_current_active_user
from applications.auth.utils.jwt import get_jwt_pair_from_user
from applications.devices.dataclasses import DeviceIdentification
from applications.users.interactors import UserInteractor
from applications.users.models import User
from applications.users.schemas import (
    BaseRetrieveUser,
    BaseUserRegister,
    BaseUserUpdate,
)
from applications.users.tasks import send_new_account_confirmation
from core.faststream_settings import faststream_broker
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from settings.manager import settings
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.transactions import in_transaction

logger = logging.getLogger(__name__)

users_router = APIRouter()


@users_router.post(
    "/register", response_model=JWTPairToken, status_code=201, tags=["users"]
)
async def register(
    *,
    user_in: BaseUserRegister,
):
    """
    Create new user.
    """
    user = await User.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    try:
        db_user = BaseUserRegister(**user_in.create_update_dict())
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    otp_code_object = await OTPCode.get_by_otp_code(db_user.otp_code)
    if not otp_code_object:
        raise HTTPException(
            status_code=400,
            detail="You've provided an invalid code. No objects associated with this code.",
        )
    if not otp_code_object.secret:
        raise HTTPException(
            status_code=400,
            detail="No secrets found related with this OTP code object.",
        )
    if not verify_otp_code(db_user.otp_code, otp_code_object.secret):
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP code.",
        )

    async with in_transaction() as conn:
        created_user = await User.register_user(db_user)
        device = await otp_code_object.device
        device.user = created_user
        device.otp_code = None
        await device.save(update_fields=("user_id", "otp_code_id"))
        await otp_code_object.delete(using_db=conn)

    if settings.EMAILS_ENABLED and user_in.email:
        await send_new_account_confirmation.kiq(user_in.email)

    await faststream_broker.publish(
        message=asdict(
            DeviceIdentification(user_id=str(created_user.pk), device_id=str(device.pk))
        ),
        queue=settings.IDENTIFICATION_TOPIC,
    )

    data = get_jwt_pair_from_user(created_user)
    return data


@users_router.patch(
    "/me", response_model=BaseRetrieveUser, status_code=200, tags=["users"]
)
async def update_user_me(
    user_data: BaseUserUpdate, current_user: User = Depends(get_current_active_user)
):
    """
    Update own user.
    """
    return await UserInteractor(current_user).update(user_data)


@users_router.post("/email/resend-verification-link", status_code=204, tags=["users"])
async def resend_verification_email_link(
    current_user: User = Depends(get_current_active_user),
):
    await UserInteractor(current_user).resend_verification_email_link()
    return {}


@users_router.get(
    "/me", response_model=BaseRetrieveUser, status_code=200, tags=["users"]
)
async def read_user_me(
    request: Request,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    user_struct = BaseRetrieveUser.model_validate(current_user)
    if user_struct.avatar:
        user_struct.avatar = urljoin(str(request.base_url), str(user_struct.avatar))
    return user_struct


@users_router.post(
    "/avatar", status_code=201, tags=["users"], response_model=BaseRetrieveUser
)
async def upload_avatar(
    avatar: UploadFile,
    request: Request,
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload avatar.
    """
    if current_user.avatar:
        try:
            current_user.avatar.delete()
        except Exception as e:
            logger.error(f"Error while deleting old avatar file: {e}")
    try:
        current_user.avatar = avatar
        await current_user.save(update_fields=["avatar"])
        await current_user.refresh_from_db(["avatar"])
        user = BaseRetrieveUser.model_validate(current_user)
        user.avatar = urljoin(str(request.base_url), str(current_user.avatar.path))
        return user
    except Exception as e:
        logger.error(f"Error while uploading avatar: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error while uploading avatar: {e}"
        )

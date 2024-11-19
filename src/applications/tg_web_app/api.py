import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

from .bot import TGWebAppBot
from .bot.enums import TGBotCommandEnum
from .bot.schemes import TelegramWebHookPayload, TGWPAQueryData
from .schemes import JWTPairTokenTgAuth
from ..auth.schemas import JWTPairToken, CredentialsSchema
from ..auth.utils.contrib import (
    get_current_active_user_with_selected_device,
    authenticate,
)
from ..auth.utils.jwt import get_jwt_pair_from_user
from ..users.interactors import UserInteractor
from ..users.models import User
from ..users.schemas.user_schemas import CreateUserTG

tg_router = APIRouter(tags=["tg"])
logger = logging.getLogger(__name__)


@tg_router.post("/webhook")
async def start_web_app_bot(data: dict) -> Response:
    data = TelegramWebHookPayload.model_validate(data)
    if data.message and not data.sender_is_bot:
        match data.bot_command:
            case TGBotCommandEnum.START:
                await TGWebAppBot.send_start_message(data.chat_id)
        return Response(status_code=200)
    return Response(status_code=200)


@tg_router.post(
    "/auth/callback/", response_model=JWTPairTokenTgAuth, status_code=201, tags=["auth"]
)
async def tg_auth_callback(
    data: TGWPAQueryData,
) -> JWTPairToken:
    user_data = data.user

    user, created = await UserInteractor().get_or_create_from_tg(
        CreateUserTG.model_validate(user_data)
    )

    data = get_jwt_pair_from_user(user)
    data["created"] = created
    return JWTPairTokenTgAuth.model_validate(data)


@tg_router.post("/merge_accounts/")
async def merge_accounts(
    credentials: CredentialsSchema,
    user_tg: User = Depends(get_current_active_user_with_selected_device),
) -> JWTPairToken:
    user_to_merge = await authenticate(credentials)

    if not user_to_merge:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    try:
        user = await UserInteractor.merge_accounts(
            user_source_pk=user_tg.id,
            user_to_merge_pk=user_to_merge.id,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400, detail="An error occurred while merging accounts."
        )

    data = get_jwt_pair_from_user(user)

    return JWTPairToken.model_validate(data)

from uuid import uuid4, UUID

from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from .bot import TGWebAppBot
from .bot.enums import TGBotCommandEnum
from .bot.schemes import TelegramWebHookPayload, TelegramAuthData
from ..auth.schemas import JWTPairToken
from ..auth.utils.jwt import get_jwt_pair_from_user
from ..users.interactors import UserInteractor
from ..users.schemas.user_schemas import CreateUserTG
from applications.users.selectors.user import UserSelector

tg_router = APIRouter(tags=["tg"])


@tg_router.post("/webhook")
async def start_web_app_bot(data: dict) -> Response:
    data = TelegramWebHookPayload.model_validate(data)
    if data.message and not data.sender_is_bot:
        match data.bot_command:
            case TGBotCommandEnum.START:
                user = await UserInteractor().get_or_create_from_tg(
                    CreateUserTG.model_validate(data.message.from_)
                )
                if not user.one_time_id:
                    user.one_time_id = uuid4()
                    await user.save(update_fields=["one_time_id"])
                await TGWebAppBot.send_start_message(
                    data.chat_id, user.one_time_id
                )
        return Response(status_code=200)
    return Response(status_code=200)


@tg_router.post("/auth/{one_time_id}")
async def auth_one_time_id(one_time_id: UUID) -> JWTPairToken:
    user = await UserSelector.get_by_one_time_id(one_time_id)
    data = get_jwt_pair_from_user(user)
    user.one_time_id = None
    await user.save(update_fields=["one_time_id"])
    return JWTPairToken.model_validate(data)

@tg_router.get(
    "/auth/callback/", response_model=JWTPairToken, status_code=201, tags=["auth"]
)
async def tg_auth_callback(
        id: str,
        first_name: str,
        hash: str,
        last_name: str | None = None,
        username: str | None = None,
        photo_url: str | None = None,
        auth_date: str | None = None,
) -> JWTPairToken:
    data = TelegramAuthData(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        photo_url=photo_url,
        auth_date=auth_date,
        hash=hash,
    )

    try:
        tg_user_data = TGWebAppBot.auth(data)
    except TGWebAppBot.TGAuthServiceAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    user = await UserInteractor().get_or_create_from_tg(
        CreateUserTG.model_validate(tg_user_data)
    )

    data = get_jwt_pair_from_user(user)
    return JWTPairToken.model_validate(data)

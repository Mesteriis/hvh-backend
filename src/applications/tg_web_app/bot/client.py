import hashlib
import hmac
import json
import logging
from urllib.parse import urljoin
from uuid import UUID

import httpx
from fastapi import FastAPI
from httpx import HTTPError

from settings.manager import settings
from .exceptions import TGWebAppBotSendError, TGAuthServiceAuthError, TGWebhookError
from .message import MSG_START_APP_ENG
from .schemes import SendMessagePayload, TelegramAuthData, TelegramUserData, InlineKeyboardMarkup, InlineKeyboardButton, \
    WebAppInfo, LinkPreviewOptions

logger = logging.getLogger(__name__)


class TGWebAppBot:
    """
    A bot for interacting with Telegram Web Apps.
    """

    __bot_token = settings.TG_WEB_APP_BOT_TOKEN
    __web_app_url = settings.WEB_APP_URL
    __secret_key = hashlib.sha256(settings.TG_WEB_APP_BOT_TOKEN.encode()).digest()

    TGWebAppBotSendError = TGWebAppBotSendError
    TGAuthServiceAuthError = TGAuthServiceAuthError
    TGWebhookError = TGWebhookError

    def __init__(self):
        """
        Initialize the TGWebAppBot with settings from the environment.
        """
        self.__bot_token = settings.TG_WEB_APP_BOT_TOKEN
        self.__web_app_url = settings.WEB_APP_URL
        self._secret_key = hashlib.sha256(self.__bot_token.encode()).digest()

    @classmethod
    def send_message(cls, data: SendMessagePayload) -> None:
        """
        Send a message to a Telegram chat.

        :param data: The data to send in the message.
        :raises TGWebAppBotSendError: If sending the message fails.
        :return: True if the message was sent successfully.
        """
        # payload = data.model_dump(exclude_unset=True, exclude_none=True)
        # payload.update('reply_markup', data.reply_markup.model_dump(exclude_unset=True, exclude_none=True))

        payload = data.model_dump(exclude_unset=True, exclude_none=True)
        try:
            response = httpx.post(
                f"https://api.telegram.org/bot{cls.__bot_token}/sendMessage",
                json=payload,
            )
        except HTTPError as exc:
            raise cls.TGWebAppBotSendError(f"Failed to send message: {exc}")

        if response.status_code != 200:  # noqa: PLR2004
            raise cls.TGWebAppBotSendError(
                f"Failed to send message: {response.json()}"
            )

    @classmethod
    async def send_start_message(cls, chat_id, one_time_id: UUID):
        """
        Send the start message to the user.

        :param chat_id: The chat ID to send the message to.
        :param text: The text to send in the message.
        :param one_time_id: The one-time ID to send in the message.
        """
        cls.send_message(
            SendMessagePayload(
                chat_id=chat_id,
                text=f"{MSG_START_APP_ENG}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=f"Start",
                                web_app=WebAppInfo(
                                    url=urljoin("https://social-front-pwa.dev.iget.mobi/tg", f'/tg/webhook/'),
                                )
                            )
                        ]
                    ]
                ),
                link_preview_options=LinkPreviewOptions(
                    url=settings.WEB_APP_URL,
                    prefer_large_media=True,
                ),
            )
        )

    @classmethod
    def init_bot(cls, app: FastAPI) -> None:
        """
        Initialize the bot with the provided FastAPI app.

        :param app: The FastAPI app to initialize the bot with.
        """
        cls.set_webapp_webhook(app)
        cls.set_menu_button(app)

    @classmethod
    def set_webapp_webhook(cls, app: FastAPI) -> None:
        """
        Set the webhook for the bot to the Web App URL.
        """

        # url = urljoin("https://social-public.dev.iget.mobi", app.url_path_for("start_web_app_bot"))
        url = urljoin("https://social-public.dev.iget.mobi", "/webhook")
        logger.info(f"Setting webhook to {url}")
        response = httpx.post(
            f"https://api.telegram.org/bot{cls.__bot_token}/setWebhook",
            params={"url": url},
        )

        if response.status_code != 200:
            raise cls.TGWebhookError(
                f"Failed to set webhook: {json.dumps(response.json())}"
            )

        logger.info(f"Webhook set successfully {url}")

    @classmethod
    def set_menu_button(cls, _: FastAPI):
        """
        Set the commands for the bot.
        """
        commands = [
            {
                "command": "start",
                "description": "https://social-front-pwa.dev.iget.mobi/tg",

            }
        ]
        response = httpx.post(
            f"https://api.telegram.org/bot{cls.__bot_token}/setMyCommands",
            json={
                "menu_button": {
                    "type": "web_app",
                    "text": "RUN",
                    "web_app": {
                        "url": urljoin(settings.WEB_APP_URL, '/tg')
                    }
                }
            }
        )

        if response.status_code != 200:
            raise cls.TGWebhookError(
                f"Failed to set commands: {json.dumps(response.json())}"
            )

        logger.info(f"Commands set successfully")

    @classmethod
    def _verify(cls, data: TelegramAuthData) -> None:
        """
        Verify the authenticity of the provided TelegramAuthData.

        :param data: The authentication data to verify.
        :raises TGAuthServiceAuthError: If the data verification fails.
        """
        data_set = []
        for key, value in data.model_dump().items():
            if value is not None:
                data_set.append(f"{key}={value}")

        data_string = "\n".join(data_set)

        hmac_hash = hmac.new(
            cls.__secret_key, data_string.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(hmac_hash, data.hash):
            raise cls.TGAuthServiceAuthError("Authorization failed")

    @classmethod
    def auth(cls, auth_data: TelegramAuthData) -> TelegramUserData:
        """
        Authenticate the provided TelegramAuthData.

        :param auth_data: The authentication data from Telegram.
        :return: Validated Telegram user data.
        :raises TGAuthServiceAuthError: If authentication fails.
        """
        cls._verify(auth_data)
        return TelegramUserData.model_validate(auth_data)

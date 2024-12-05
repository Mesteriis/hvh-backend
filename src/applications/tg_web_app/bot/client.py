import json
import logging
from urllib.parse import urljoin

import httpx
from fastapi import FastAPI
from httpx import HTTPError
from settings.manager import settings

from .exceptions import TGAuthServiceAuthError, TGWebAppBotSendError, TGWebhookError
from .message import MSG_START_APP_ENG
from .schemes import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    SendMessagePayload,
    WebAppInfo,
)

logger = logging.getLogger(__name__)


class TGWebAppBot:
    """
    A bot for interacting with Telegram Web Apps.
    """

    __bot_token = settings.TG_WEB_APP_BOT_TOKEN
    __web_app_url = settings.WEB_APP_URL
    __backend_domain = settings.BACKEND_DOMAIN

    TGWebAppBotSendError = TGWebAppBotSendError
    TGAuthServiceAuthError = TGAuthServiceAuthError
    TGWebhookError = TGWebhookError

    @classmethod
    def send_message(cls, data: SendMessagePayload) -> None:
        """
        Send a message to a Telegram chat.

        :param data: The data to send in the message.
        :raises TGWebAppBotSendError: If sending the message fails.
        :return: True if the message was sent successfully.
        """

        payload = data.model_dump(exclude_unset=True, exclude_none=True)
        try:
            response = httpx.post(
                f"https://api.telegram.org/bot{cls.__bot_token}/sendMessage",
                json=payload,
            )
        except HTTPError as exc:
            raise cls.TGWebAppBotSendError(f"Failed to send message: {exc}")

        if response.status_code != 200:  # noqa: PLR2004
            raise cls.TGWebAppBotSendError(f"Failed to send message: {response.json()}")

    @classmethod
    async def send_start_message(cls, chat_id):
        """
        Send the start message to the user.

        :param chat_id: The chat ID to send the message to.
        """
        cls.send_message(
            SendMessagePayload(
                chat_id=chat_id,
                text=f"{MSG_START_APP_ENG}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Start",
                                web_app=WebAppInfo(
                                    url=urljoin(cls.__web_app_url, "/tg"),
                                ),
                            )
                        ]
                    ]
                ),
                link_preview_options=LinkPreviewOptions(
                    url=cls.__web_app_url,
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
        try:
            cls.set_webapp_webhook(app)
        except cls.TGWebhookError as exc:
            logger.error(f"Failed to set webhook: {exc}")

    @classmethod
    def set_webapp_webhook(cls, app: FastAPI) -> None:
        """
        Set the webhook for the bot to the Web App URL.
        """
        url = urljoin(cls.__backend_domain, app.url_path_for("start_web_app_bot"))
        logger.info(f"Setting webhook to {url}")
        response = httpx.post(
            f"https://api.telegram.org/bot{cls.__bot_token}/setWebhook",
            params={"url": url},
        )

        if response.status_code != 200:
            if response.status_code == 429 and response.json()["description"] == "Too Many Requests: retry after 1":
                return
            raise cls.TGWebhookError(f"Failed to set webhook url:{url}, error:\n {json.dumps(response.json())}")
        else:
            logger.info(f"Webhook set successfully {url}")

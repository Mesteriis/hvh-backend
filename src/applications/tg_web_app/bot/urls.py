from pydantic import BaseModel

from settings.manager import settings


class BotUrls(BaseModel):
    _base_url: str = "https://api.telegram.org/bot"
    __bot_token: str = settings.TG_WEB_APP_BOT_TOKEN
    SEND_MESSAGE: str = "sendMessage"
    SET_WEBHOOK: str = "setWebhook"
    SET_BOT_MENU_BUTTON: str = "setBotMenuButton"

    def __getattr__(self, item):
        return f"{self._base_url}{self.__bot_token}/{getattr(self, item)}"

from settings.manager import settings
from .message import LAUNCH_APP_ENG


MARKUP = {
    "keyboard": [
        [
            {
                "text": LAUNCH_APP_ENG,
                "web_app": {"url": settings.WEB_APP_URL},
            },
        ]
    ],
    "resize_keyboard": False,
    "one_time_keyboard": True,
}
REPLY_MARKUP = {
    "inline_keyboard": [
        [
            {
                "text": LAUNCH_APP_ENG,
                "web_app": {"url": settings.WEB_APP_URL},
            }
        ]
    ],
}

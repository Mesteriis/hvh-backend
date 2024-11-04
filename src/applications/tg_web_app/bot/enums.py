from enum import Enum


class TGBotCommandEnum(str, Enum):
    START = "/start"


class ParseModeEnum(Enum):
    MARKDOWN = 'Markdown'
    MARKDOWN_V2 = 'MarkdownV2'
    HTML = 'HTML'

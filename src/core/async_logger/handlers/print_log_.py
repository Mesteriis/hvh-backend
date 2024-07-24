from colorama import init as colorama_init, Style

from ..abstract import ABCHandler
from ..constants import NAMED_LOG_LEVEL_COLOR


class PrintLog(ABCHandler):
    """
    PrintLog — это вызываемый класс, который выводит сообщения на консоль.
    """

    name = "PrintLog"

    def __call__(self, msg):
        """
        Выводит на консоль отформатированное сообщение лога.

        Форматирует сообщение лога с использованием цвета и метаданных в
        зависимости от уровня. Печатает отформатированное сообщение на консоль.
        Также печатает все трассировки исключений.
        """
        colorama_init()
        format_ = NAMED_LOG_LEVEL_COLOR[msg.level]

        print(
            f'{format_.fore or ""}'
            f'{format_.back or ""}'
            f'|x-request-id -> {msg.request_headers.get("x-request-id", None)}'
            f"|[{msg.timestamp}]  "
            f"|{msg.thread}  "
            f"|{msg.level_name}  "
            f"|{msg.request_method} "
            f"|{msg.message}\n"
            f'|user-agent -> {msg.request_headers.get("user-agent", None)}\n'
            f"|request_body -> {msg.request_body}\n"
            f"|response_body -> {msg.response_body}\n"
            f"{Style.RESET_ALL} ",
        )

        if msg.exceptions:
            for el in msg.exceptions:
                print(el, end="")

from colorama import Back, Fore

from .structures.log_level_color import LogLevelStringColor

NAMED_LOG_LEVEL = {
    0: "NOT_SET",
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
}

NAMED_LOG_LEVEL_COLOR = {
    0: LogLevelStringColor(level_name="NOT_SET", fore=None, back=None),
    10: LogLevelStringColor(level_name="DEBUG", fore=Fore.WHITE, back=None),
    20: LogLevelStringColor(level_name="INFO", fore=Fore.LIGHTGREEN_EX, back=None),
    30: LogLevelStringColor(level_name="WARNING", fore=Fore.YELLOW, back=None),
    40: LogLevelStringColor(level_name="ERROR", fore=Fore.LIGHTRED_EX, back=None),
    50: LogLevelStringColor(level_name="CRITICAL", back=Back.RED),
}

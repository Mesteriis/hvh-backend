from logging import getLogger


class ConsoleLogger:
    __logger = getLogger("MediaDownloader")

    @classmethod
    def debug(cls, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            cls.__logger.debug(msg)
        else:
            cls.info(msg)

    @classmethod
    def info(cls, msg):
        cls.__logger.info(msg)

    @classmethod
    def warning(cls, msg):
        cls.__logger.warning(msg)

    @classmethod
    def error(cls, msg):
        cls.__logger.exception(msg)

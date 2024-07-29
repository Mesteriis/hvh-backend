from logging import getLogger


class ConsoleLogger:
    __logger = getLogger("MediaDownloader")

    @classmethod
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            self.__logger.debug(msg)
        else:
            self.info(msg)

    @classmethod
    def info(self, msg):
        self.__logger.info(msg)

    @classmethod
    def warning(self, msg):
        self.__logger.warning(msg)

    @classmethod
    def error(self, msg):
        self.__logger.exception(msg)

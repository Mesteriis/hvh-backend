import logging

logger = logging.getLogger(__name__)


class TGWebAppBotSendError(Exception):
    """
    Exception raised when sending a message via the bot fails.
    """

    def __init__(self, message):
        """
        Initialize the TGWebAppBotSendError with an error message.

        :param message: The error message.
        """
        self.message = message
        logger.error(message)
        super().__init__(message)


class TGAuthServiceAuthError(Exception):
    """
    Exception raised when Telegram authentication fails.
    """


class TGWebhookError(Exception):
    """
    Exception raised when setting up a webhook fails.
    """

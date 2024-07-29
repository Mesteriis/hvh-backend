import logging

from ..structs import DownloadItemState

logger = logging.getLogger(__name__)


def console_hook(data: dict) -> None:
    logger.info(str(DownloadItemState.model_validate(data)))

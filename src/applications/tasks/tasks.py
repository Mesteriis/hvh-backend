import uuid

from celery import shared_task

from applications.tasks.service import TaskSelector
from applications.youtube.service import YTVideoInteractor, YTChannelInteractor, YTPlaylistInteractor, YTVideoSelector, \
    YTChannelSelector, YTPlaylistSelector
from tools.media_downloader.downloader import MediaDownloader


@shared_task
async def parse_url(task_id: uuid.UUID) -> None:
    task = await TaskSelector.get_by_id(task_id)
    service = MediaDownloader.download(task.url)
    info = service.extract_info()

    if service.source == "youtube":
        if service.url.is_video:
            selector = YTVideoSelector
            interactor = YTVideoInteractor
        elif service.url.is_channel:
            selector = YTChannelSelector
            interactor = YTChannelInteractor
        else:
            selector = YTPlaylistSelector
            interactor = YTPlaylistInteractor

        raw_data = info.model_dump(by_alias=False)

        if item := await selector.get_by_ext_id(service.url):
            await interactor.update(item.pk, {"meta_data": raw_data})
        else:
            await interactor.create(raw_data)

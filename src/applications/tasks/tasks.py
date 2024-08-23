import uuid

from applications.tasks.service import TaskSelector
from applications.youtube.models import YTVideoModel, YTChannelModel, YTPlaylistModel
from applications.youtube.service import YTItemInteractor, YTItemSelector
from celery import shared_task

from applications.youtube.structs import YTItemStruct
from tools.media_downloader.downloader import MediaDownloader


@shared_task
async def parse_url(task_id: uuid.UUID) -> None:
    task = await TaskSelector.get_by_id(task_id)
    service = MediaDownloader.download(task.url)
    info = service.extract_info()

    if service.source == "youtube":
        if service.is_video:
            service.model = YTVideoModel
        if service.is_channel:
            service.model = YTChannelModel
        if service.is_playlist:
            service.model = YTPlaylistModel

        selector = YTItemSelector(service.model)
        interactor = YTItemInteractor(service.model)

        raw_data = info.model_dump(by_alias=False)

        if item := await selector.get_by_ext_id(info.id):
            await interactor.set_metadata(item.pk, raw_data)
        else:
            await interactor.create(
                YTItemStruct.model_validate({
                    "owner": task.owner,
                    "task": task,
                    "ext_id": info.id,
                    "meta_data": raw_data
                })
            )

import uuid
from abc import ABC
from typing import Type

from applications.tasks.structs import Task, TaskInDB
from .models import YTVideo, YTChannel, YTPlaylist


class YTItemSelector:

    @classmethod
    async def get_by_id(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], item_id: uuid.UUID):
        return await model.objects.get(pk=item_id)

    @classmethod
    async def get_by_ext_id(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], ext_id: str):
        return await model.objects.get(ext_id=ext_id)

    @classmethod
    async def get_all(cls, model) -> list[TaskInDB]:
        items = await model.objects.all()
        return [TaskInDB.model_validate(item) for item in items]

    @classmethod
    async def get_by_owner(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], owner_id: uuid.UUID) -> list[TaskInDB]:
        items = await model.objects.filter(owner_id=owner_id)
        return [TaskInDB.model_validate(item) for item in items]

    @classmethod
    async def get_by_status(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], status: str) -> list[TaskInDB]:
        items = await model.objects.filter(status=status)
        return [TaskInDB.model_validate(item) for item in items]


class BaseYTItemInteractor(ABC):
    __model = None

    @classmethod
    async def create(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], data: Task):
        data = data.model_dump()
        item = await model.objects.create(url=str(data["url"]), owner_id=data["owner_id"])
        return TaskInDB.model_validate(item)

    @classmethod
    async def delete(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], item_pk: uuid.UUID) -> None:
        item = await model.objects.get(pk=item_pk)
        await item.delete()

    @classmethod
    async def update(cls, model: Type[YTVideo] | Type[YTChannel] | Type[YTPlaylist], item_pk: uuid.UUID, data: dict) -> None:
        item = await model.objects.get(pk=item_pk)
        await item.update(**data).apply()

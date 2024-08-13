import uuid
from abc import ABC
from typing import Type

from .models import YTVideoModel, YTChannelModel, YTPlaylistModel
from .structs import YTItemStruct


class YTItemSelector:

    @classmethod
    async def get_by_id(
            cls,
            model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel],
            item_id: uuid.UUID,
            as_model: bool = False
    ) -> YTVideoModel | YTChannelModel | YTPlaylistModel | YTItemStruct:
        if as_model:
            return await model.objects.get(pk=item_id)
        return YTItemStruct.model_validate(
            await model.objects.get(pk=item_id)
        )

    @classmethod
    async def get_by_ext_id(
            cls,
            model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel],
            ext_id: str
    ) -> Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]:
        return await model.objects.get(ext_id=ext_id)

    @classmethod
    async def get_all(cls, model) -> list[Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]]:
        return await model.objects.all()

    @classmethod
    async def get_by_owner(
            cls,
            model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel],
            owner_id: uuid.UUID
    ) -> list[Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]]:
        return await model.objects.filter(owner_id=owner_id)

    @classmethod
    async def get_by_status(
            cls,
            model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel],
            status: str
    ) -> list[Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]]:
        return await model.objects.filter(status=status)


class YTItemInteractor(ABC):
    __model = None

    @classmethod
    async def create(cls, model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel], data: dict):
        data = data.model_dump()
        item = await model.objects.create(url=str(data["url"]), owner_id=data["owner_id"])
        return TaskInDB.model_validate(item)

    @classmethod
    async def delete(cls, model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel],
                     item_pk: uuid.UUID) -> None:
        item = await model.objects.get(pk=item_pk)
        await item.delete()

    @classmethod
    async def update(cls, model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel], item_pk: uuid.UUID,
                     data: dict) -> None:
        item = await model.objects.get(pk=item_pk)
        await item.update(**data).apply()

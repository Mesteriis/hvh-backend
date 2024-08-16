import uuid
from typing import Type

from .models import YTVideoModel, YTChannelModel, YTPlaylistModel
from .structs import YTItemStruct


class YTItemSelector:
    __model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]

    def __init__(self, model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]):
        self.__model = model

    async def get_by_id(
            self,
            item_id: uuid.UUID,
            as_model: bool = False
    ) -> YTVideoModel | YTChannelModel | YTPlaylistModel | YTItemStruct:
        if as_model:
            return await self.__model.objects.get(pk=item_id)
        return YTItemStruct.model_validate(
            await self.__model.objects.get(pk=item_id)
        )

    async def get_by_ext_id(
            self,
            ext_id: str
    ) -> YTVideoModel | YTChannelModel | YTPlaylistModel:
        return await self.__model.objects.get(ext_id=ext_id)

    async def get_all(self) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.all()

    async def get_by_owner(
            self,
            owner_id: uuid.UUID
    ) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.filter(owner_id=owner_id)

    async def get_by_status(
            self,
            status: str
    ) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.filter(status=status)


class YTItemInteractor:
    __model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]

    def __init__(self, model: Type[YTVideoModel] | Type[YTChannelModel] | Type[YTPlaylistModel]):
        self.__model = model

    async def create(self, data: YTItemStruct):
        return await self.__model.objects.create(**data.model_dump())

    async def delete(self, item_pk: uuid.UUID) -> None:
        item = await self.__model.objects.get(pk=item_pk)
        await item.delete()

    async def update(self, item_pk: uuid.UUID, data: YTItemStruct) -> None:
        item = await self.__model.objects.get(pk=item_pk)
        await item.update(**data.model_dump(exclude_none=true)).apply()

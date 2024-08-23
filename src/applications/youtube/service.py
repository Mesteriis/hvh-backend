import uuid

from .models import YTChannelModel, YTPlaylistModel, YTVideoModel
from .structs import YTItemStruct


class YTItemSelector:
    __model: type[YTVideoModel] | type[YTChannelModel] | type[YTPlaylistModel]

    def __init__(self, model: type[YTVideoModel] | type[YTChannelModel] | type[YTPlaylistModel]):
        self.__model = model

    async def get_by_id(
        self, item_id: uuid.UUID, as_model: bool = False
    ) -> YTVideoModel | YTChannelModel | YTPlaylistModel | YTItemStruct:
        if as_model:
            return await self.__model.objects.get(pk=item_id)
        return YTItemStruct.model_validate(await self.__model.objects.get(pk=item_id))

    async def get_by_ext_id(self, ext_id: str) -> YTVideoModel | YTChannelModel | YTPlaylistModel:
        return await self.__model.objects.get(ext_id=ext_id)

    async def get_all(self) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.all()

    async def get_by_owner(self, owner_id: uuid.UUID) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.filter(owner_id=owner_id)

    async def get_by_status(self, status: str) -> list[YTVideoModel | YTChannelModel | YTPlaylistModel]:
        return await self.__model.objects.filter(status=status)


class YTItemInteractor:
    __model: type[YTVideoModel] | type[YTChannelModel] | type[YTPlaylistModel]

    def __init__(self, model: type[YTVideoModel] | type[YTChannelModel] | type[YTPlaylistModel]):
        self.__model = model

    async def create(self, data: YTItemStruct) -> YTItemStruct:
        return YTItemStruct.model_validate(
            await self.__model.objects.create(
                **data.model_dump(exclude={"owner", "task"}), owner_id=data.owner.id, task_id=data.task.id
            )
        )

    async def set_metadata(self, item_id: uuid.UUID, data) -> YTItemStruct:
        item = await self.__model.objects.get(pk=item_id)
        await item.update(meta_data=data)
        item.status = "parsed"
        return YTItemStruct.model_validate(item)

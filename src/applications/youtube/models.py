from tools.base_db_model import BaseDBModel
from tortoise import fields

from .enums import StatusEnum


class BaseYTItemModel(BaseDBModel):
    owner = fields.ForeignKeyField("models.UserModel", related_name="items")
    task = fields.ForeignKeyField("models.TaskModel", related_name="tasks")
    metadata = fields.JSONField(null=False, default={})
    status = fields.CharEnumField(StatusEnum, default=StatusEnum.new, index=True)
    ext_id = fields.CharField(max_length=256, index=True, unique=True)

    class Meta:
        abstract = True


class YTChannelModel(BaseYTItemModel):
    class Meta:
        table = "channels"

    owner = fields.ForeignKeyField("models.UserModel", related_name="channels")
    task = fields.ForeignKeyField("models.TaskModel", related_name="channels")


class YTPlaylistModel(BaseYTItemModel):
    class Meta:
        table = "playlists"

    owner = fields.ForeignKeyField("models.UserModel", related_name="playlists")
    task = fields.ForeignKeyField("models.TaskModel", related_name="playlists")


class YTVideoModel(BaseYTItemModel):
    class Meta:
        table = "videos"

    owner = fields.ForeignKeyField("models.UserModel", related_name="videos")
    task = fields.ForeignKeyField("models.TaskModel", related_name="videos")

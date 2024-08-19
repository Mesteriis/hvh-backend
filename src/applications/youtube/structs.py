import uuid

from pydantic import BaseModel, ConfigDict, Field
from setuptools.command.alias import alias

from applications.tasks.structs import TaskInBaseStruct
from applications.users.schemas.user_schemas import UserInBaseStruct
from applications.youtube.enums import StatusEnum


class YTItemStruct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    owner: UserInBaseStruct
    task: TaskInBaseStruct
    meta_data: dict | None = None
    status: StatusEnum = StatusEnum.new
    ext_id: str | None = None

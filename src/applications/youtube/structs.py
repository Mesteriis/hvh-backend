from pydantic import BaseModel, ConfigDict

from applications.tasks.structs import TaskInBaseStruct
from applications.users.schemas.user_schemas import UserInBaseStruct
from applications.youtube.enums import StatusEnum


class YTItemStruct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    owner: UserInBaseStruct
    task: TaskInBaseStruct
    meta_data: dict
    status: StatusEnum
    ext_id: str

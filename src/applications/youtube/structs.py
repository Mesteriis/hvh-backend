from applications.tasks.structs import TaskInBaseStruct
from applications.users.schemas.user_schemas import UserInBaseStruct
from applications.youtube.enums import StatusEnum
from pydantic import BaseModel, ConfigDict


class YTItemStruct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    owner: UserInBaseStruct
    task: TaskInBaseStruct
    meta_data: dict | None = None
    status: StatusEnum = StatusEnum.new
    ext_id: str | None = None

from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class TaskStruct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    url: AnyHttpUrl = Field(
        ...,
        alias="url",
    )
    owner_id: UUID


class TaskInBaseStruct(TaskStruct):
    id: UUID


class TaskCreateStruct(TaskStruct):
    owner_id: None = None


class TaskResponse(TaskInBaseStruct):
    pass

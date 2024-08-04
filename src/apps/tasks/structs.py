from uuid import UUID

from pydantic import BaseModel, ConfigDict, AnyHttpUrl, Field


class Task(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    url: AnyHttpUrl = Field(..., alias="url", )
    owner_id: UUID


class TaskInDB(Task):
    id: UUID


class TaskCreate(Task):
    owner_id: None = None

class TaskResponse(TaskInDB):
    pass



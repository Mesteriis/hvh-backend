from uuid import UUID

from pydantic import BaseModel, ConfigDict, AnyHttpUrl


class Task(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    url: AnyHttpUrl
    owner_id: UUID


class TaskInDB(Task):
    id: UUID


class TaskCreate(Task):
    owner_id: None = None

class TaskResponse(TaskInDB):
    pass



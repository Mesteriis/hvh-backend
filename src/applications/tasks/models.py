from enum import Enum

from tools.base_db_model import BaseDBModel
from tortoise import fields


class TaskStatusEnum(Enum):
    new = "new"
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskModel(BaseDBModel):
    url = fields.CharField(max_length=256, index=True)
    owner = fields.ForeignKeyField("models.UserModel", related_name="tasks")
    status = fields.CharEnumField(TaskStatusEnum, default=TaskStatusEnum.new)

    def __repr__(self) -> str:
        return f"<TaskModel id={self.id} url={self.url} status={self.status}>"

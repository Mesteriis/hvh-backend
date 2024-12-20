import uuid

from applications.tasks.models import TaskModel
from applications.tasks.structs import TaskInBaseStruct, TaskStruct


class TaskSelector:
    @classmethod
    async def get_by_id(cls, task_id: uuid.UUID) -> TaskInBaseStruct:
        return TaskInBaseStruct.model_validate(await TaskModel.get(pk=task_id))

    @classmethod
    async def get_by_id_and_owner(cls, task_id: uuid.UUID, owner_id: uuid.UUID) -> TaskInBaseStruct:
        return TaskInBaseStruct.model_validate(await TaskModel.get(pk=task_id, owner_id=owner_id))

    @classmethod
    async def get_all(cls) -> list[TaskInBaseStruct]:
        tasks = await TaskModel.all()
        return [TaskInBaseStruct.model_validate(task) for task in tasks]

    @classmethod
    async def get_by_owner(cls, owner_id: uuid.UUID) -> list[TaskInBaseStruct]:
        tasks = await TaskModel.filter(owner_id=owner_id)
        return [TaskInBaseStruct.model_validate(task) for task in tasks]


class TaskInteractor:
    @classmethod
    async def create(cls, data: TaskStruct) -> TaskInBaseStruct:
        data = data.model_dump()
        task = await TaskModel.create(url=str(data["url"]), owner_id=data["owner_id"])
        return TaskInBaseStruct.model_validate(task)

    @classmethod
    async def delete(cls, task_pk: uuid.UUID) -> None:
        task = await TaskModel.get(pk=task_pk)
        await task.delete()

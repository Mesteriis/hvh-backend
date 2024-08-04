import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from apps.tasks.models import TaskModel
from apps.tasks.structs import TaskInDB
# from apps.users.models import UserModel


class TaskSelector:
    @classmethod
    async def get_by_id(cls, task_id: int, db: AsyncSession) -> TaskInDB:
        return TaskInDB.model_validate(
            await db.execute(
                select(TaskModel).where(TaskModel.id == task_id).first()
            )
        )

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[TaskInDB]:
        query = select(TaskModel)
        result = await db.execute(query)
        tasks = result.scalars().all()
        return [TaskInDB.model_validate(task) for task in tasks]


class TaskInteractor:
    @classmethod
    async def create(cls, url: str, db: AsyncSession, user) -> TaskInDB:
        task = TaskModel(
            url=url,
            owner_id=user.id
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return TaskInDB.model_validate(task)

    @classmethod
    async def delete(cls, task_pk: uuid.UUID, db: AsyncSession) -> None:
        query = delete(TaskModel).where(TaskModel.id == task_pk)
        await db.execute(query)
        await db.commit()

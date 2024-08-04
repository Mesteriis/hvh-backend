from sqlalchemy import select

from apps.tasks.models import TaskModel
from apps.tasks.service import TaskSelector, TaskInteractor
from apps.tasks.structs import Task


class TestTaskSelector:

    async def test_get_all(self, task_factory, user_factory):
        user = await user_factory.create()
        await task_factory.create_batch(5, owner_id=user.id)
        tasks = await TaskSelector.get_all()
        assert len(tasks) >= 5

    async def test_get_by_id(self, task_factory, user_factory):
        user = await user_factory.create()
        tasks = await task_factory.create_batch(5, owner_id=user.id)
        task = await TaskSelector.get_by_id(tasks[0].id)
        assert task.id == tasks[0].id

    async def test_get_by_id_and_owner(self, task_factory, user_factory):
        user = await user_factory.create()
        tasks = await task_factory.create_batch(5, owner_id=user.id)
        task = await TaskSelector.get_by_id_and_owner(tasks[0].id, user.id)
        assert task.id == tasks[0].id

    async def test_get_by_owner(self, task_factory, user_factory):
        user = await user_factory.create()
        await task_factory.create_batch(5, owner_id=user.id)
        tasks = await TaskSelector.get_by_owner(user.id)
        assert len(tasks) == 5



class TestTaskInteractor:

    async def test_create(self, user_factory):
        user = await user_factory.create()
        task = await TaskInteractor.create(
            Task(url="https://example.com", owner_id=user.id)
        )
        assert task.owner_id == user.id

    async def test_delete(self, session, user_factory, task_factory):
        user = await user_factory.create()
        task = await task_factory.create(
            owner_id=user.id
        )
        pk = task.id
        await TaskInteractor.delete(pk)
        query = select(TaskModel).where(TaskModel.id == pk)
        task_in_db = await session.execute(query)
        assert task_in_db.fetchone() is None
        await session.commit()

import pytest
from tortoise.exceptions import DoesNotExist

from applications.tasks.models import TaskModel
from applications.tasks.service import TaskSelector, TaskInteractor
from applications.tasks.structs import TaskStruct


async def test_get_all(task_factory, user_factory):
    user = await user_factory.create()
    await task_factory.create_batch(5, owner_id=user.id)
    tasks = await TaskSelector.get_all()
    assert len(tasks) >= 5


async def test_get_by_id(task_factory, user_factory):
    user = await user_factory.create()
    tasks = await task_factory.create_batch(5, owner_id=user.id)
    task = await TaskSelector.get_by_id(tasks[0].id)
    assert task.id == tasks[0].id


async def test_get_by_id_and_owner(task_factory, user_factory):
    user = await user_factory.create()
    tasks = await task_factory.create_batch(5, owner_id=user.id)
    task = await TaskSelector.get_by_id_and_owner(tasks[0].id, user.id)
    assert task.id == tasks[0].id


async def test_get_by_owner(task_factory, user_factory):
    user = await user_factory.create()
    await task_factory.create_batch(5, owner_id=user.id)
    tasks = await TaskSelector.get_by_owner(user.id)
    assert len(tasks) == 5


async def test_create(user_factory):
    user = await user_factory.create()
    task = await TaskInteractor.create(
        TaskStruct(url="https://example.com", owner_id=user.id)
    )
    assert str(task.owner_id) == str(user.id)


async def test_delete(user_factory, task_factory):
    user = await user_factory.create()
    task = await task_factory.create(
        owner_id=user.id
    )
    pk = task.id
    await TaskInteractor.delete(pk)
    with pytest.raises(DoesNotExist):
        await TaskModel.get(pk=pk)

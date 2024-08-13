import uuid

from applications.tasks.service import TaskInteractor, TaskSelector
from applications.tasks.structs import TaskCreateStruct, TaskResponse
from applications.users.auth.depens import current_user
from applications.users.models import UserModel
from fastapi import APIRouter, Depends

tasks_router = APIRouter(tags=["tasks"])


@tasks_router.get("/", response_model=list[TaskResponse])
async def get_list_tasks(
    user: UserModel = Depends(current_user),
):
    if user.is_superuser:
        return await TaskSelector.get_all()
    else:
        return await TaskSelector.get_by_owner(user.pk)


@tasks_router.post("/", response_model=TaskResponse)
async def create_task(
    data: TaskCreateStruct,
    user: UserModel = Depends(current_user),
):
    data.owner_id = user.id
    return await TaskInteractor.create(data)


@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    user: UserModel = Depends(current_user),
):
    if user.is_superuser:
        return await TaskSelector.get_by_id(task_id)
    else:
        return await TaskSelector.get_by_id_and_owner(task_id, user.id)

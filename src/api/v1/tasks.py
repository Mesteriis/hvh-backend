import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.tasks.service import TaskSelector, TaskInteractor
from apps.tasks.structs import TaskResponse, TaskCreate
from apps.users.dependens import current_active_user
from config.db import get_session

tasks_router = APIRouter(tags=["tasks"])


@tasks_router.get("/", response_model=list[TaskResponse])
async def get_list_tasks(
        db: AsyncSession = Depends(get_session),
        user=Depends(current_active_user)
):
    return await TaskSelector.get_all(db)


@tasks_router.post("/", response_model=TaskResponse)
async def create_task(
        data: TaskCreate,
        db: AsyncSession = Depends(get_session),
        user=Depends(current_active_user)
):
    return await TaskInteractor.create(str(data.url), db, user)


@tasks_router.get("/{task_id}")
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return {"tasks": {}}

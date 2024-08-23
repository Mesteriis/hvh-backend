__all__ = ["v1_router"]

from fastapi import APIRouter

from .tasks import tasks_router
from .user_views import users_router

v1_router = APIRouter()
v1_router.include_router(
    tasks_router,
    prefix="/tasks",
)
v1_router.include_router(
    users_router,
    prefix="/users",
)

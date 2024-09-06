__all__ = ["v1_router"]

from fastapi import APIRouter

from .auth_views import auth_router
from .sse_views import router_sse
from .tasks_views import tasks_router
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
v1_router.include_router(
    auth_router,
    prefix="/auth",
)
v1_router.include_router(
    router_sse,
    prefix="/sse",
)

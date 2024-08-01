__all__ = ["api_v1_router"]

from fastapi import APIRouter

from .v1 import v1_router

api_v1_router = APIRouter(prefix="/api")
api_v1_router.include_router(
    v1_router,
    prefix="/v1",
)

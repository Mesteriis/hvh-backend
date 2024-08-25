import logging
from uuid import UUID

from applications.users.interactors import UserInteractor

from fastapi import APIRouter, Depends

from applications.users.models import UserModel
from applications.users.schemas.user_schemas import UserRegisterStruct, UserInBaseStruct, UserUpdateStruct
from applications.users.selectors import UserSelector
from applications.users.auth.depens import current_user, superuser

logger = logging.getLogger(__name__)

users_router = APIRouter()


#
@users_router.post("/register", response_model=UserInBaseStruct, status_code=201, tags=["users"])
async def register(
        user_in: UserRegisterStruct,
) -> UserInBaseStruct:
    """
    Create new user.
    """
    user = await UserInteractor.registry_user(user_in)
    return UserInBaseStruct.model_validate(user)


@users_router.get('/', response_model=list[UserInBaseStruct], status_code=200, tags=["users"])
async def get_users(
        _: UserModel = Depends(current_user),
) -> list[UserInBaseStruct]:
    """
    Get all users.
    """
    users = await UserSelector.get_all()
    return [UserInBaseStruct.model_validate(user) for user in users]


@users_router.get('/me', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def get_user_me(
        user: UserModel = Depends(current_user),
) -> UserInBaseStruct:
    """
    Get current user.
    """
    return UserInBaseStruct.model_validate(user)


@users_router.post('/me', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def update_me(
        user_data: UserUpdateStruct,
        user: UserModel = Depends(current_user),
) -> UserInBaseStruct:
    """
    Get current user.
    """
    user = await UserInteractor.update(user.id, user_data)
    return UserInBaseStruct.model_validate(user)


@users_router.get('/{user_id}', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def get_user_by_id(
        user_id: UUID,
        _: UserModel = Depends(current_user),
) -> UserInBaseStruct:
    """
    Get user by id.
    """
    user = await UserSelector.get_by_uid(user_id)
    return UserInBaseStruct.model_validate(user)


@users_router.patch('/{user_id}', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def update_user_by_id(
        user_id: UUID,
        user_data: UserUpdateStruct,
        _: UserModel = Depends(superuser),
) -> UserInBaseStruct:
    """
    Update user by id.
    """
    return UserInBaseStruct.model_validate(
        await UserInteractor.update(user_id, user_data)
    )


@users_router.post('/{user_id}/block', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def block_user_by_id(
        user_id: UUID,
        _: UserModel = Depends(superuser),
) -> UserInBaseStruct:
    """
    Block user by id.
    """
    return UserInBaseStruct.model_validate(
        await UserInteractor.block_user(user_id)
    )


@users_router.post('/{user_id}/block', response_model=UserInBaseStruct, status_code=200, tags=["users"])
async def unblock_user_by_id(
        user_id: UUID,
        _: UserModel = Depends(superuser),
) -> UserInBaseStruct:
    """
    Block user by id.
    """
    return UserInBaseStruct.model_validate(
        await UserInteractor.unblock_user(user_id)
    )

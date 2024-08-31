
import pytest

from applications.users.interactors import UserInteractor
from applications.users.schemas.user_schemas import UserRegisterStruct, UserUpdateStruct
from core.config import settings

pytestmark = pytest.mark.unit

async def test_registry_user():
    user_data = {
        "email": 'test_email@email.com',
        "password": 'test_password',
        "password_confirmation": 'test_password'
    }
    user = await UserInteractor.registry_user(
        data=UserRegisterStruct.model_validate(user_data)
    )
    assert user.email == user_data['email']
    assert user.is_active != settings.id_account_verification

async def test_update_user(user_factory):
    user = await user_factory.create()
    user_data = {
        "first_name": 'New First Name',
    }
    user = await UserInteractor.update(user.id, UserUpdateStruct.model_validate(user_data))
    assert user.first_name == user_data['first_name'], f'Expected {user_data["first_name"]}, got {user.email}'


async def test_block_user(user_factory):
    user = await user_factory.create()
    user = await UserInteractor.block_user(user.id)
    assert not user.is_active, f'Expected False, got {user.is_active}'


async def test_unblock_user(user_factory):
    user = await user_factory.create(is_active=False)
    user = await UserInteractor.unblock_user(user.id)
    assert user.is_active, f'Expected True, got {user.is_active}'

import pytest

from applications.users.interactors import UserInteractor
from applications.users.schemas.user_schemas import UserRegisterStruct

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


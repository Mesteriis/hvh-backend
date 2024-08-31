import pytest

from applications.users.auth.utils.contrib import generate_password_reset_token
from applications.users.auth.utils.password import verify_and_update_password
from applications.users.interactors import PasswordInteractor
from applications.users.models import UserModel
from applications.users.schemas import ResetPasswordSchema

pytestmark = pytest.mark.unit


@pytest.mark.skip
async def test_reset_password(user_factory):
    user = await user_factory.create()
    new_password = 'new_password'
    token = generate_password_reset_token(user.email)
    await PasswordInteractor.reset_password(
        ResetPasswordSchema(
            password=new_password, password_confirmation=new_password, reset_token=token)
    )
    user = await UserModel.objects.get(pk=user.pk)
    verify_, hash_password = verify_and_update_password(new_password, user.hashed_password)
    assert verify_

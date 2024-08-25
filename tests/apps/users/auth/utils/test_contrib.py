import pytest
from faker import Faker

from applications.users.auth.schemas import CredentialsSchema
from applications.users.auth.utils.contrib import generate_password_reset_token, verify_password_reset_token, \
    authenticate

pytestmark = pytest.mark.unit

faker = Faker()


def test_generate_password_reset_token():
    email = faker.email()
    token = generate_password_reset_token(email)
    assert token
    assert isinstance(token, str)
    assert token.count(".") == 2


def test_verify_password_reset_token():
    email = faker.email()
    token = generate_password_reset_token(email)
    email_ = verify_password_reset_token(token)
    assert email == email_


async def test_authenticate(user_factory):
    user = await user_factory.create()
    password = faker.password(
        length=12,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
    await user.set_password(password)
    user_data = CredentialsSchema(
        email=user.email,
        password=password
    )
    user_ = await authenticate(user_data)
    assert user.pk == user_.pk


@pytest.mark.skip(reason="Not implemented")
def test_reusable_oauth2():
    assert True

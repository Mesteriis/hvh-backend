
import pytest

from applications.users.selectors import UserSelector

pytestmark = pytest.mark.unit


async def test_get_by_pk(user_factory):
    user = await user_factory.create()
    user_in_base = await UserSelector.get_by_uid(user.pk)
    assert user.pk == user_in_base.pk
    assert user.email == user_in_base.email


async def test_get_by_email(user_factory):
    user = await user_factory.create()
    user_in_base = await UserSelector.get_by_email(user.email)
    assert user.pk == user_in_base.pk
    assert user.email == user_in_base.email
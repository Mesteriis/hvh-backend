import pytest

from applications.users.models import UserModel
from core.config import settings
from tests.inventory import assert_response

pytestmark = pytest.mark.api


async def test_registry_user(client):
    user_data = {
        "email": 'test@test.ru',
        "password": 'test_password',
        "password_confirmation": 'test_password'
    }
    url = client.url_for('register')
    response = await client.post(url, json=user_data)
    assert_response(response, 201, data={
        'email': user_data['email'],
        'is_active': settings.id_account_verification == False
    })


async def test_get_users(client, user_factory):
    users = await user_factory.create_batch(3)
    url = client.url_for('get_users')
    await client.force_auth(users[0])
    response = await client.get(url)
    assert_response(response)
    data = response.json()
    assert len(data) >= 3


async def test_get_user_me(client):
    user = await client.force_auth()
    url = client.url_for('get_user_me')
    response = await client.get(url)
    assert_response(response, 200, {
        'email': user.email,
        'is_active': user.is_active
    })


async def test_update_me(client):
    user = await client.force_auth()
    last_name = user.last_name
    url = client.url_for('update_me')
    data = {
        'first_name': 'same_new_name'
    }
    response = await client.post(url, json=data)
    assert_response(response, 200)
    data_ = response.json()
    user = await UserModel.objects.get(pk=user.pk)
    assert data_['first_name'] == data['first_name']
    assert user.first_name == data['first_name']
    assert user.last_name == last_name


async def test_get_user_by_id(client, user_factory):
    user = await user_factory()
    url = client.url_for('get_user_by_id', user_id=user.id)
    await client.force_auth(is_superuser=True)
    response = await client.get(url)
    assert_response(response, 200, {
        'email': user.email,
        'is_active': user.is_active
    })


async def test_update_user_by_id(client, user_factory):
    affected_user = await user_factory.create()
    await client.force_auth(is_superuser=True)
    url = client.url_for('update_user_by_id', user_id=affected_user.pk)
    payload = {
        'first_name': 'new_name',
    }
    response = await client.patch(url, json=payload)
    assert_response(response, 200, payload)



async def test_block_user_by_id(client, user_factory):
    affected_user = await user_factory.create()
    await client.force_auth(is_superuser=True)
    url = client.url_for('block_user_by_id', user_id=affected_user.pk)
    response = await client.post(url)
    assert_response(response, 200, {
        "is_active": False
    })

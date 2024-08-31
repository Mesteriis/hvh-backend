import faker
import pytest

from tests.inventory import assert_response

pytestmark = pytest.mark.api

faker = faker.Faker()
async def test_access_token(client, user_factory):
    user = await user_factory.create()
    password = faker.password(
        length=12,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
    await user.set_password(password)
    user_data = {
        "email": user.email,
        "password": password
    }
    url = client.url_for('access_token')
    response = await client.post(url, json=user_data)
    assert_response(response, 200)
    data = response.json()
    assert 'access' in data, f"Expected 'access' in response, got {data}"
    assert 'access_expiration_at' in data, f"Expected 'access_expiration_at' in response, got {data}"
    assert 'refresh' in data, f"Expected 'refresh' in response, got {data}"
    assert 'refresh_expiration_at' in data, f"Expected 'refresh_expiration_at' in response, got {data}"
    assert 'user_id' in data, f"Expected 'user_id' in response, got {data}"

async def test_access_token_invalid_credentials(client, user_factory):
    user = await user_factory.create()
    user_data = {
        "email": user.email,
        "password": faker.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
    }
    url = client.url_for('access_token')
    response = await client.post(url, json=user_data)
    assert_response(response, 400)
    data = response.json()
    assert 'detail' in data, f"Expected 'detail' in response, got {data}"
    assert data['detail'] == "Incorrect email or password", f"Expected 'Incorrect email or password' in response, got {data}"

async def test_access_token_inactive_user(client, user_factory):
    user = await user_factory.create(is_active=False)
    password = faker.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
    await user.set_password(password)
    user_data = {
        "email": user.email,
        "password": password
    }
    url = client.url_for('access_token')
    response = await client.post(url, json=user_data)
    assert_response(response, 400)
    data = response.json()
    assert 'detail' in data, f"Expected 'detail' in response, got {data}"
    assert data['detail'] == "Inactive user", f"Expected 'Inactive user' in response, got {data}"

async def test_refresh(client, user_factory):
    user = await user_factory.create()
    password = faker.password(
        length=12,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
    await user.set_password(password)
    user_data = {
        "email": user.email,
        "password": password
    }
    url = client.url_for('access_token')
    response = await client.post(url, json=user_data)
    assert_response(response, 200)
    data = response.json()
    assert 'refresh' in data, f"Expected 'refresh' in response, got {data}"
    refresh_data = {
        "refresh": data['refresh']
    }
    url = client.url_for('refresh')
    response = await client.post(url, json=refresh_data)
    assert_response(response, 200)
    data = response.json()
    assert 'access' in data, f"Expected 'access' in response, got {data}"
    assert 'access_expiration_at' in data, f"Expected 'access_expiration_at' in response, got {data}"
    assert 'refresh' in data, f"Expected 'refresh' in response, got {data}"
    assert 'refresh_expiration_at' in data, f"Expected 'refresh_expiration_at' in response, got {data}"
    assert 'user_id' in data, f"Expected 'user_id' in response, got {data}"
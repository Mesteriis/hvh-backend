import uuid
from datetime import timedelta

import pytest

from applications.users.auth.utils.jwt import create_access_token, create_refresh_token, get_jwt_pair_from_user, \
    get_jwt_pair_with_userid_from_refresh_token

pytestmark = pytest.mark.unit


def assert_token(token):
    assert token
    assert token.encoded_jwt, "Expected encoded_jwt to be set"
    assert token.exp, "Expected exp to be set"
    assert token.iat, "Expected iat to be set"
    assert token.encoded_jwt.startswith("eyJ"), "Expected encoded_jwt to be a JWT"
    assert token.encoded_jwt.count(".") == 2, "Expected encoded_jwt to have 2 parts"
    assert token.exp > token.iat, "Expected exp to be greater than iat"
    assert token.exp - token.iat == 900000, "Expected exp to be 15 minutes after iat"


def test_create_access_token():
    token = create_access_token(
        data={"user_id": "1"},
        expires_delta=timedelta(minutes=15)
    )
    assert_token(token)


def test_create_refresh_token():
    token = create_refresh_token(
        data={"user_id": "1"},
        expires_delta=timedelta(minutes=15)
    )
    assert_token(token)


async def test_get_jwt_pair_from_user(user_factory):
    user = await user_factory.create()
    data = get_jwt_pair_from_user(user)
    assert 'access' in data, f"Expected 'access' in response, got {data}"
    assert 'access_expiration_at' in data, f"Expected 'access_expiration_at' in response, got {data}"
    assert 'refresh' in data, f"Expected 'refresh' in response, got {data}"
    assert 'refresh_expiration_at' in data, f"Expected 'refresh_expiration_at' in response, got {data}"


def test_get_jwt_pair_with_userid_from_refresh_token():
    user_id = str(uuid.uuid4())
    refresh = create_refresh_token(
        data={"user_id": user_id},
        expires_delta=timedelta(minutes=15)
    )
    data = get_jwt_pair_with_userid_from_refresh_token(refresh.encoded_jwt)
    assert 'access' in data, f"Expected 'access' in response, got {data}"
    assert 'access_expiration_at' in data, f"Expected 'access_expiration_at' in response, got {data}"
    assert 'refresh' in data, f"Expected 'refresh' in response, got {data}"
    assert 'refresh_expiration_at' in data, f"Expected 'refresh_expiration_at' in response, got {data}"
    assert 'user_id' in data, f"Expected 'user_id' in response, got {data}"
    assert data['user_id'] == user_id, f"Expected 'user_id' to be '1', got {data['user_id']}"

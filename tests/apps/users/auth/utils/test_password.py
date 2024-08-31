import pytest

from applications.users.auth.utils.password import get_password_hash, verify_and_update_password

pytestmark = pytest.mark.unit


def test_verify_and_update_password():
    plain_password = "test_password"
    hashed_password = 'pbkdf2_sha256$600000$eAfjni91oSNGepe+i6/wdw==$JY5i64U8aSW3dxs8JFd4ooJWqvx0/cLMGT/hfi+b6/I='
    verified, new_hash = verify_and_update_password(plain_password, hashed_password)
    assert verified


def test_get_password_hash():
    password = "test_password"
    hashed_password = get_password_hash(password)
    assert hashed_password

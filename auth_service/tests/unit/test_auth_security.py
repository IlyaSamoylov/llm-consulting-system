import pytest

from app.core.security import (
	hash_password,
	verify_password,
	create_access_token,
	decode_token
)

@pytest.mark.unit
def test_hash_password_not_equal_to_plain_password():
    password = "StrongPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False

@pytest.mark.unit
def test_create_and_decode_access_token():
    payload_in = {"sub": "123", "role": "admin"}

    token = create_access_token(**payload_in)
    payload_out = decode_token(token)

    assert payload_out["sub"] == "123"
    assert payload_out["role"] == "admin"
    assert "iat" in payload_out
    assert "exp" in payload_out
    assert payload_out["exp"] > payload_out["iat"]
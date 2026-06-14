import pytest
from jose import jwt
from datetime import datetime, timezone, timedelta

from app.core.config import settings
from app.core.jwt import decode_and_validate

@pytest.mark.unit
def test_decode_and_validate_returns_payload_sub():
	token = jwt.encode({
		"sub": "test_user",
		"exp": datetime.now(timezone.utc) + timedelta(minutes=10)
	},
	settings.JWT_SECRET,
	algorithm=settings.JWT_ALG
	)

	payload = decode_and_validate(token)

	assert payload["sub"] == "test_user"

@pytest.mark.unit
def test_decode_and_validate_rejects_garbage_str():
	with pytest.raises(ValueError):
		decode_and_validate("this_is_a_garbage_string")

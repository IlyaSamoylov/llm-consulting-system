from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

from app.core.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
	"""Функция хэширования пароля"""
	return pwd_context.hash(password)

def verify_password(password: str, truth: str) -> bool:
	"""Верификация пароля"""
	return pwd_context.verify(password, truth)

def create_access_token(*, sub: str, role: str) -> str:
	"""Создание JWT токена"""
	iat = datetime.now(timezone.utc)
	exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	payload = {
		"sub": str(sub),
		"role": role,
		"iat": int(iat.timestamp()),
		"exp": exp
	}

	return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALG)

def decode_access_token(token: str) -> dict[str, str]:
	"""Декодирование токена"""
	try:
		payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
	except ExpiredSignatureError as exc:
		raise TokenExpiredError() from exc
	except JWTError as exc:
		raise InvalidTokenError() from exc

	if "sub" not in payload:
		raise InvalidTokenError()

	return payload
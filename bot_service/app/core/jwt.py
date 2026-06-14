from jose import jwt, ExpiredSignatureError, JWTError

from app.core.config import settings

def decode_and_validate(token: str) -> dict:
	"""Проверяет подпись, exp и возвращает payload токена"""
	try:
		payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

	except ExpiredSignatureError as exc:
		raise ValueError("Токен просрочен") from exc
	except JWTError as exc:
		raise ValueError(f"Невалидный токен.") from exc

	if "exp" not in payload:
		raise ValueError("Токен не содержит exp")
	if "sub" not in payload:
		raise ValueError("Токен не содержит sub")

	return payload
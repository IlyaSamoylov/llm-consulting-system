from fastapi import HTTPException, status

class BaseHTTPException(HTTPException):
	"""Базовая http ошибка приложения"""
	def __init__(self, status_code: int, detail: str):
		super().__init__(status_code, detail)

class InvalidTokenError(BaseHTTPException):
	def __init__(self, detail: str = "Некорректный JWT токен"):
		super().__init__(status.HTTP_401_UNAUTHORIZED, detail)

class TokenExpiredError(BaseHTTPException):
	def __init__(self, detail: str = "Истекший JWT токен"):
		super().__init__(status.HTTP_401_UNAUTHORIZED, detail)

class UserAlreadyExist(BaseHTTPException):
	def __init__(self, detail: str = "Пользователь с таким email уже существует"):
		super().__init__(status.HTTP_409_CONFLICT, detail)

class InvalidCredentials(BaseHTTPException):
	def __init__(self, detail: str ="Неверные учетные данные"):
		super().__init__(status.HTTP_401_UNAUTHORIZED, detail)

class UserNotFoundError(BaseHTTPException):
	def __init__(self, detail: str = "Пользователь не найден"):
		super().__init__(status.HTTP_404_NOT_FOUND, detail)
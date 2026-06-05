from fastapi import HTTPException, status

class BaseHTTPException(HTTPException):
	def __init__(self, status_code: int, detail: str):
		super().__init__(status_code, detail)

class InvalidTokenError(BaseHTTPException):
	def __init__(self, detail: str = "Некорректный JWT токен"):
		super().__init__(status.HTTP_401_UNAUTHORIZED, detail)

class TokenExpiredError(BaseHTTPException):
	def __init__(self, detail: str = "Истекший JWT токен"):
		super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
	"""Схема запроса на регистрацию пользователя"""
	email: EmailStr = Field(max_length=255)
	password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
	"""Схема запроса на вход пользователя"""
	email: EmailStr = Field(max_length=255)
	password: str = Field(min_length=8, max_length=128)

class TokenResponse(BaseModel):
	"""Схема ответа при успешной аутентификации"""
	access_token: str
	token_type: str = "bearer"
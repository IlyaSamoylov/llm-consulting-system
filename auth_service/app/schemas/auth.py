from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
	"""Схема запроса на регистрацию пользователя"""
	email: EmailStr
	password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
	"""Схема запроса на вход пользователя"""
	email: EmailStr
	password: str = Field(min_length=8, max_length=128)
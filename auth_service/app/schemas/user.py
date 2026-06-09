from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserPublic(BaseModel):
	"""Схема публичного профиля пользователя"""
	model_config = ConfigDict(from_attributes=True)

	id: int = Field(ge=1)
	email: EmailStr = Field(max_length=255)
	role: str = Field(max_length=25)
	created_at: datetime

from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError
from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
	"""Генерация сессии бд"""
	async with AsyncSessionLocal() as session:
		yield session

def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
	"""Фабрика репозитория пользователей"""
	return UserRepository(db)

def get_auth_uc(users_repo: UserRepository = Depends(get_user_repo)) -> AuthUsecase:
	"""Фабрика usecase аутентификации"""
	return AuthUsecase(users_repo)

async def get_current_user_id(token: str | None = Depends(oauth2_scheme)) -> int:
	"""Извлекает и валидирует id пользователя из токена"""
	if not token:
		raise InvalidTokenError("Нет bearer-токена")

	payload = decode_access_token(token)
	sub = payload.get("sub")
	if sub is None:
		raise InvalidTokenError("В токене отсутствует 'sub'")

	try:
		return int(sub)
	except (TypeError, ValueError) as exc:
		raise InvalidTokenError("Невалидный токен") from exc

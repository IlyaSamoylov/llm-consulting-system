from sqlalchemy.exc import IntegrityError
from app.db.models import User

from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.exceptions import UserAlreadyExist, InvalidCredentials, UserNotFoundError

class AuthUsecase:
	def __init__(self, users_repo: UserRepository):
		self.users_repo = users_repo

	async def register(self, data: RegisterRequest):
		existing = await self.users_repo.get_by_email(str(data.email))
		if existing:
			raise UserAlreadyExist()

		pwd_hash = hash_password(data.password)
		try:
			return await self.users_repo.create(email=str(data.email), pwd_hash=pwd_hash)
		except IntegrityError as exc:
			await self.users_repo.rollback()
			raise UserAlreadyExist() from exc

	async def login(self, data: LoginRequest) -> str:
		user = await self.users_repo.get_by_email(str(data.email))
		if not user:
			raise InvalidCredentials()

		if not verify_password(data.password, user.password_hash):
			raise InvalidCredentials()

		return create_access_token(sub=str(user.id), role=user.role)

	async def me(self, *, uid: int) -> User:
		user = await self.users_repo.get_by_id(uid)
		if not user:
			raise UserNotFoundError()
		return user

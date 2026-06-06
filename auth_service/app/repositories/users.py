from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User

class UserRepository:
	def __init__(self, db: AsyncSession):
		self.db = db

	async def get_by_id(self, user_id: int) -> User | None:
		stmt = select(User).where(User.id == user_id)
		res = await self.db.execute(stmt)
		return res.scalars().one_or_none()

	async def get_by_email(self, email: str) -> User | None:
		stmt = select(User).where(User.email == email)
		res = await self.db.execute(stmt)
		return res.scalars().one_or_none()

	async def create(self, *, email: str, pwd_hash: str, role: str = "user") -> User:
		user = User(email=email, password_hash=pwd_hash, role=role)
		self.db.add(user)
		await self.db.commit()
		print(f"У нового пользователя id: {user.id}, создан: {user.created_at}")
		return user

	async def rollback(self):
		await self.db.rollback()
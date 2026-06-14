from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
	"""ORM-модель пользователя"""
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
	password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
	role: Mapped[str] = mapped_column(String(25), nullable=False, default="user")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False
	)
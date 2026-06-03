from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import settings

class Database:
	def __init__(self, url: str | None = None):
		self.url = url or self._build_postgres_url()

		self.engine = create_async_engine(
			settings.db_url,
		    echo=settings.AUTH_DEBUG,
		    future=True,
		    pool_pre_ping=True
		)

		self.AsyncSessionLocal = async_sessionmaker(
			self.engine,
		    class_=AsyncSession,
		    autoflush=False,
		    autocommit=False,
		    expire_on_commit=False,
		    future=True
		)


	def _build_postgres_url(self) -> str:
		"""Database url"""
		return settings.db_url

db = Database()
engine = db.engine
AsyncSessionLocal = db.AsyncSessionLocal
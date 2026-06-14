import os

# если задавать переменные окружения через shell/Docker/etc, нужен формат `os.environ["DB_USER"] = "test_user"`
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "1234")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test_db")

from fastapi import FastAPI
from app.api.error_handlers import register_exception_handlers
from app.api.router import api_router
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.db.base import Base
from app.api.deps import get_db

@pytest_asyncio.fixture
async def engine():
	engine = create_async_engine(settings.db_url, echo=False)

	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	yield engine

	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)

	await engine.dispose()

@pytest.fixture
def session_factory(engine):
	return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
def test_app(session_factory):
	async def override_get_db():
		async with session_factory() as session:
			yield session

	app = FastAPI(title=settings.APP_NAME)
	register_exception_handlers(app)
	app.include_router(api_router)

	app.dependency_overrides[get_db] = override_get_db
	yield app
	app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client(test_app):
	async with AsyncClient(
			transport=ASGITransport(app=test_app),
			base_url="http://test"
	) as client:
		yield client

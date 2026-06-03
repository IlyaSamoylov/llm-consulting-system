from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание таблицы пользователей до запуска"""
    async with engine.begin() as conn:
        print("Tables before create_all:", Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Проверка статуса сервиса"""
    return {"service": settings.APP_NAME, "status": "ok"}
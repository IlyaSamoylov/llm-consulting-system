from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.error_handlers import register_exception_handlers
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание таблицы пользователей до запуска"""
    async with engine.begin() as conn:
        print("На запуске созданы таблицы:", Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
register_exception_handlers(app)
app.include_router(api_router)

@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Проверка статуса сервиса"""
    return {"service": settings.APP_NAME, "status": "ok"}
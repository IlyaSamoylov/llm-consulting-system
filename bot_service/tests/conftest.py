import pytest
import os
from typing import Callable
from types import SimpleNamespace
from unittest.mock import AsyncMock

class MemoryRedis:

	def __init__(self):
		self._store: dict[str, str] = {}

	async def get(self, key: str) -> str | None:
		return self._store.get(key)

	async def set(self, key: str, value: str) -> bool:
		self._store[key] = value
		return True

	async def delete(self, key: str) -> int:
		existed = key in self._store
		self._store.pop(key, None)
		return int(existed)

@pytest.fixture
def fake_redis() -> MemoryRedis:
	return MemoryRedis()

@pytest.fixture
def patch_handlers_redis(monkeypatch: pytest.MonkeyPatch, fake_redis: MemoryRedis) -> MemoryRedis:
	import app.bot.handlers as handlers

	monkeypatch.setattr(handlers, "get_redis", lambda: fake_redis)
	return fake_redis

@pytest.fixture
def make_message() -> Callable:
	def _make_message(
			text: str,
			user_id: int = 1,
			chat_id: int = 2,
			with_user: bool = True,
			with_chat: bool = True
	):
		return SimpleNamespace(
			text=text,
			from_user=SimpleNamespace(id=user_id) if with_user else None,
			chat=SimpleNamespace(id=chat_id) if with_chat else None,
			answer=AsyncMock()
		)
	return _make_message
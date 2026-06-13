from redis import Redis

from app.core.config import settings

_redis_client: Redis | None = None

def get_redis() -> Redis:
	"""
	Единая точка получения Redis-клиента. При первом обращении создает новый, дальше
	переиспользует его же
	"""
	global _redis_client

	if _redis_client is None:
		_redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
	return _redis_client
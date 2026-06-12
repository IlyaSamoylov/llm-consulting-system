from celery import Celery

from app.core.config import settings

celery_app = Celery(
	settings.APP_NAME,
	broker=settings.RABBITMQ_URL,
	backend=settings.REDIS_URL,
	include=["app.tasks.llm_tasks"]
)

celery_app.conf.update(
	task_serializer="json",
	result_serializer="json",
	accept_content=["json"],
	task_default_queue="llm"
)

celery_app.autodiscover_tasks(["app.tasks"])
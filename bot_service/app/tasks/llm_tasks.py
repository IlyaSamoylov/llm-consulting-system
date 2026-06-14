import logging
import httpx

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter, OpenRouterError

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.llm_tasks.llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str | None:
	"""Celery-задача, получает ответ от OpenRouter, формирует ответ и отправляет сообщение пользователю"""

	try:
		llm_answer = call_openrouter(prompt)
	except OpenRouterError as exc:
		llm_answer = f"Ошибка LLM: {exc}"

	if not settings.BOT_TOKEN:
		logger.warning("Токен бота телеграм не задан, пропускаю")
		return

	url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
	payload = {"chat_id": tg_chat_id, "text": llm_answer}

	try:
		with httpx.Client(timeout=20.0) as client:
			response = client.post(url, json=payload)
			response.raise_for_status()
	except httpx.HTTPError:
		logger.exception("Не удалось отправить сообщение из Celery worker")

	return llm_answer
import logging
import httpx

from app.core.config import settings
from app.infra.celery_app import celery_app

# TODO: наверное, полезно попробовать использовать logger еще в других местах и в auth-service тоже
logger = logging.getLogger(__name__)

# TODO: Заменить на реальный ответ из openrouter_client
def call_openrouter_sync(prompt) -> str:
	"""Заглушка вместо ответа от OpenRouter"""
	return "Какой-то ответ LLM"

class OpenrouterError(RuntimeError):
	pass

@celery_app.task(name="app.tasks.llm_tasks.llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
	try:
		llm_answer = call_openrouter_sync(prompt)
	except OpenrouterError as exc:
		llm_answer = f"Ошибка LLM: {exc}"

	_send_telegram_message(tg_chat_id=tg_chat_id, text=llm_answer)
	return llm_answer

def _send_telegram_message(*, tg_chat_id: int, text: str):
	if not settings.TELEGRAM_BOT_TOKEN:
		logger.warning("Токен бота телеграм не задан, пропускаю")
		return

	url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
	payload = {"chat_id": tg_chat_id, "text": text}

	try:
		with httpx.Client(timeout=20.0) as client:
			response = client.post(url, json=payload)
			response.raise_for_status()
	except httpx.HTTPError:
		logger.exception("Не удалось отправить сообщение из Celery worker")
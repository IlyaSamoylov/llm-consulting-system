from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()

def _redis_key(uid: int) -> str:
	return f"token:{uid}"

@router.message(CommandStart())
async def start_command(message: Message):
	"""Начальное сообщение"""
	await message.answer("Бот открывает доступ к LLM OpenRouter по JWT-токену. "
	                     "Сначала отправьте свой токен командой: /token <JWT>")


@router.message(Command("token"))
async def auth_command(message: Message):
	"""Получает Jwt-токен, валидирует, сохраняет в Redis"""

	if not message.from_user:
		await message.answer("Невозможно идентифицировать id пользователя")
		return

	text = message.text or ""
	parts = text.split(maxsplit=1)
	if len(parts) < 2:
		await message.answer("Используйте: /token <JWT>")
		return

	token = parts[1].strip()
	try:
		decode_and_validate(token)
	except ValueError:
		await message.answer("Токен сломан или истек. Получите новый в auth-сервисе")
		return

	redis_instance = get_redis()
	await redis_instance.set(_redis_key(message.from_user.id), token)
	await message.answer("Токен сохранен. Теперь вы можете отправлять сообщения модели")

@router.message()
async def message_handler(message: Message):
	"""Обработчик сообщений - проверяет токен, отправляет запрос LLM"""

	if not message.text or message.text.startswith("/"):
		return
	if not message.from_user or not message.chat:
		await message.answer("Ошибка обработки: отсутствуют метаданные пользователя")
		return

	redis_instance = get_redis()
	redis_key = _redis_key(message.from_user.id)
	token = await redis_instance.get(redis_key)

	if not token:
		await message.answer(
			"Токен не найден. Авторизуйтесь в auth-сервисе и отправьте токен с командой /token <JWT>")
		return

	try:
		decode_and_validate(token)
	except ValueError:
		await redis_instance.delete(redis_key)
		await message.answer(
			"Токен невалидный или просрочен. Авторизуйтесь в auth-сервисе и отправьте /token <JWT>")
		return

	llm_request.delay(message.chat.id, message.text)
	await message.answer("Запрос успешно отправлен LLM")
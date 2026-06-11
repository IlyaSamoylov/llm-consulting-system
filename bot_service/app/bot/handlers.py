from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis

router = Router()
TOKEN_KEY_PREFIX = "token:"

def _token_key(uid: int) -> str:
	return f"{TOKEN_KEY_PREFIX}{uid}"

@router.message(CommandStart())
async def start_command(message: Message):
	await message.answer("Бот открывает доступ к LLM по JWT-токену. "
	                     "Сначала отправьте свой токен командой: /token <JWT>")

async def handle_auth_command(message: Message, redis_client=None):
	text = (message.text or "").strip()
	parts = text.split(maxsplit=1)
	if len(parts) < 2:
		await message.answer("Использовать: /token <JWT>")
		return

	token = parts[1]
	try:
		decode_and_validate(token)
	except ValueError:
		await message.answer("Токен сломан или истек. Получите новый в auth-сервисе")
		return

	if not message.from_user:
		await message.answer("Невозможно идентифицировать id пользователя")
		return

	redis_instance = redis_client or get_redis()
	await redis_instance.set(_token_key(message.from_user.id), token)
	await message.answer("Токен сохранен. Теперь вы можете отправлять сообщения модели")

@router.message(Command("token"))
async def auth_command(message: Message):
	await handle_auth_command(message)

async def handle_message(message: Message, redis_client=None):
	if not message.text:
		return
	if message.text.startswith("/"):
		return
	if not message.from_user or not message.chat:
		await message.answer("Ошибка обработки: отсутствуют метаданные пользователя")
		return

	redis_instance = redis_client or get_redis()
	redis_key = _token_key(message.from_user.id)
	token = await redis_instance.get(redis_key)

	if not token:
		await message.answer("Токен не найден. Авторизуйтесь в auth-сервисе и отправьте токен с командой /token <JWT>")
		return

	try:
		payload = decode_and_validate(token)
	except ValueError:
		await redis_instance.delete(redis_key)
		await message.answer("Токен невалидный или просрочен. Авторизуйтесь в auth-сервисе и отправьте /token <JWT>")
		return
	# TODO: Добавить llm_request.delay
	await message.answer("Запрос успешно отправлен LLM")

@router.message()
async def message_handler(message: Message):
	await handle_message(message)
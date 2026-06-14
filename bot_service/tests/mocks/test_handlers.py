import pytest
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings
import app.bot.handlers as handlers

def _make_valid_token(sub: str = "test_user") -> str:
	return jwt.encode(
		{
			"sub": sub,
			"exp": datetime.now(timezone.utc) + timedelta(minutes=10)
		},
		settings.JWT_SECRET,
		algorithm=settings.JWT_ALG
	)

@pytest.mark.mock
async def test_token_command_saves_token_in_fake_redis(patch_handlers_redis, make_message):
	token = _make_valid_token()
	message = make_message(f"/token {token}", user_id=777, chat_id=888)

	await handlers.auth_command(message)

	saved = await patch_handlers_redis.get("token:777")
	assert saved == token
	message.answer.assert_awaited_once()
	assert "Токен сохранен" in message.answer.await_args.args[0]

@pytest.mark.mock
async def test_message_handler_without_token_doesnt_call_celery(patch_handlers_redis, make_message, mocker):
	delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")
	message = make_message("Привет, бот!", user_id=1, chat_id=2)
	await handlers.message_handler(message)

	delay_mock.assert_not_called()
	message.answer.assert_awaited_once()
	assert "Токен не найден" in message.answer.await_args.args[0]

@pytest.mark.mock
async def test_message_handler_with_token_calls_celery_and_answers(
	patch_handlers_redis,
	make_message,
	mocker,
):
	token = _make_valid_token(sub="user-101")
	await patch_handlers_redis.set("token:101", token)

	delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

	message = make_message("Сделай краткое резюме", user_id=101, chat_id=303)
	await handlers.message_handler(message)

	delay_mock.assert_called_once_with(303, "Сделай краткое резюме")
	message.answer.assert_awaited_once()
	assert "Запрос успешно отправлен" in message.answer.await_args.args[0]

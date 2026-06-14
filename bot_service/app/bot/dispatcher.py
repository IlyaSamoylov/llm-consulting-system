from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.bot.handlers import router


def create_dispatcher() -> tuple[Bot, Dispatcher]:
	"""Сборка и регистрация обработчиков"""
	bot = Bot(token=settings.BOT_TOKEN)
	dispatcher = Dispatcher()
	dispatcher.include_router(router)
	return bot, dispatcher
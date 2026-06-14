import asyncio

from app.bot.dispatcher import create_dispatcher

async def run_bot():
	bot, dispatcher = create_dispatcher()
	await dispatcher.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(run_bot())
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.rethinkdb import RethinkDBStorage

from handlers.order import register_handlers_order
from handlers.common import register_handlers_common

async def set_commands(bot: Bot):

	commands = [
		BotCommand(command="/order", description="Оформить заказ"),
		BotCommand(command="/cancel", description="Отменить текущее действие")
	]
	await bot.set_my_commands(commands)
	
async def main():

	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)
	logger.error("Starting bot")
		
	bot = Bot(token=config.tg_bot.token)
	
	dp = Dispatcher(bot, storage=RethinkDBStorage(
					db='aiogram', 
					table='aiogram', 
					user='aiogram', 
					password='aiogram_secret')
					)
					
	register_handlers_order(dp)
	register_handlers_common(dp)
	
	await set_commands(bot)
	
	await dp.start_polling()
	
if __name__ == '__main__':
	asyncio.run(main())

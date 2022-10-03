import asyncio
import logging
import configparser

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.rethinkdb import RethinkDBStorage

from handlers.order import register_handlers_order
#from handlers.common import register_handlers_common

logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):

	commands = [
		BotCommand(command="/start", description="Начало работы"),
		#BotCommand(command="/cancel", description="Отменить текущее действие")
	]
	await bot.set_my_commands(commands)
	
async def main():

	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)
	logger.error("Starting bot")
		
	config = configparser.ConfigParser()
	config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/token.ini')
	bot = Bot(token=config.get('token', 'bot_token'))
	
	dp = Dispatcher(bot, storage=RethinkDBStorage(
					db='aiogram', 
					table='aiogram', 
					user='aiogram', 
					password='aiogram_secret')
					)
					
	register_handlers_order(dp)
	#register_handlers_common(dp)
	
	await set_commands(bot)
	
	await dp.start_polling()
	
if __name__ == '__main__':
	asyncio.run(main())

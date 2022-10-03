import asyncio
import logging
import configparser

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.rethinkdb import RethinkDBStorage

from handlers.totalAmountBot_handlers import register_handlers_totalAmount
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
	config.read('/home/koza/Reps/totalAmountCalculator_rep/application/token.ini')
	bot = Bot(token=config.get('token', 'bot_token'))
	
	dp = Dispatcher(bot, storage=RethinkDBStorage(
					db='totalAmountBot_db', 
					table='totalAmountBot_table', 
					user='totalAmountBot_user', 
					password='totalAmountBot_user_pswd')
					)
					
	register_handlers_totalAmount(dp)
	
	await set_commands(bot)
	
	await dp.start_polling()
	
if __name__ == '__main__':
	asyncio.run(main())

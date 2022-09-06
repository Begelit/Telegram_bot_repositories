from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

async def cmd_start(message: types.Message, state: FSMContext):
	await state.finish()
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('Оформить заказ')
	await bot.delete_message(message.chat.id,message['message_id'])
	msg = await message.answer('Привет! Отправь /order или нажми "Оформить заказ".',reply_markup=keyboard)#+
				#'\n\n Чтобы отменить действие отправь /cancel.',reply_markup=keyboard)#+
				#'\n\n Чтобы получить список команд отправь /help.',reply_markup=keyboard)
	async with state.proxy() as data:
		#data['msgs_id'] = dict()
		data['start_msgs_id'] = msg['message_id']
		
				
	
#async def cmd_cancel(message: types.Message, state: FSMContext):
#	await state.finish()
#	await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
	
#async def cmd_help(message: types.Message, state: FSMContext):
#	await state.finish()

def register_handlers_common(dp: Dispatcher):
	dp.register_message_handler(cmd_start, commands="start", state="*")
	#dp.register_message_handler(cmd_cancel, commands="cancel", state="*")

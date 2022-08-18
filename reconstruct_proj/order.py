from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import parser
import asyncio
lock = asyncio.Lock()

class OrderClothes(StatesGroup):
	waiting_for_clothes_url = State()
	waiting_for_clothes_color = State()
	waiting_for_clothes_size = State()

async def order_start(message: types.Message):
	await message.answer("Пожалуйста, отправьте ссылку, ведущую на товар.")
	await OrderClothes.waiting_for_clothes_url.set()

async def color_chosen(message: types.Message, state: FSMContext):
	
	await state.update_data(received_url=message.text)

	await message.answer("Пожалуйста, подождите.")

	driver_path = '/home/koza/Reps/HEIN_FROMgit/shein_bot/drivers/chromedriver'
	url = message.text
	driver = parser.start_driverSession(driver_path=driver_path)
	
	async with lock:
		driver_getSource = parser.get_page_source(driver,url)
		await asyncio.sleep(3)
	product_info = parser.get_product_info(driver_getSource)
	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for color in product_info:
		keyboard.add(color)
		
	await OrderFood.waiting_for_clothes_color.set()
	
	await message.answer("Укажите нужный цвет:", reply_markup=keyboard)
	
	

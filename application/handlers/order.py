from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from handlers.parserANDdb import parser 
import asyncio

lock = asyncio.Lock()

class OrderClothes(StatesGroup):
	waiting_for_clothes_url = State()
	waiting_for_clothes_color = State()
	waiting_for_clothes_size = State()
	waiting_for_confirm = State()

async def order_start(message: types.Message):
	await message.answer("Пожалуйста, отправьте ссылку, ведущую на товар.")
	await OrderClothes.waiting_for_clothes_url.set()

async def clothes_chosen(message: types.Message, state: FSMContext):
	
	await state.update_data(received_url=message.text)

	await message.answer("Пожалуйста, подождите.")

	url = message.text

	driver_path = '/home/koza/Reps/drivers/chromedriver'
	driver = parser.start_driverSession(driver_path=driver_path)
	
	async with lock:
		driver_getSource = parser.get_page_source(driver,url)
		await asyncio.sleep(3)
	product_info = parser.get_product_info(driver_getSource)
	#print(product_info)
	
	#await state.update_data(productDetail=product_info)
	driver.close()
	
	async with state.proxy() as data:
		data['productDetail'] = product_info
		
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for color in product_info['color']:
		keyboard.add(color)
		
	await OrderClothes.waiting_for_clothes_color.set()
	await message.answer("Укажите нужный цвет:", reply_markup=keyboard)
	
async def color_chosen(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		order_data = data
	#print(order_data)
	colors_list = [color for color in order_data['productDetail']['color']]
	if message.text not in colors_list:
		await message.answer('Пожалуйста, введите нужный цвет, используя клавиатуру ниже:')
		return
	async with state.proxy() as data:
		data['received_color'] = message.text
	#await state.update_data(received_color=message.text)
	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	#print(order_data)
	for size in order_data['productDetail']['color'][message.text]['size']:
		keyboard.add(size)
	
	await OrderClothes.waiting_for_clothes_size.set()
	await message.answer("Теперь выберите размер:", reply_markup=keyboard)
	
async def size_order(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		order_data = data
	#order_data = await state.get_data()
	color = order_data['received_color']
	size = order_data['productDetail']['color'][color]['size']
	if message.text not in size:
		await message.answer('Пожалуйста, введите нужный размер, используя клавиатуру ниже:')
		return
	async with state.proxy() as data:
		data['received_size'] = message.text
		order_data = data
	print(order_data)
	#await state.update_data(received_size=message.text)
	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('Подтвердить')
	keyboard.add('Отменить')
	
	await OrderClothes.waiting_for_confirm.set()
	await message.answer("Почти готово! Пожалуйста, подтвердите заказ:"
				f"\n\n  {order_data['productDetail']['name']}"
				f"\n    Цвет: {order_data['received_color']}"
				f"\n    Размер: {order_data['received_size']}"
				f"\n    Цена: {order_data['productDetail']['color'][order_data['received_color']]['price']}",reply_markup=keyboard)
	
async def confirm_order(message: types.Message, state: FSMContext):
	if message.text not in ['Подтвердить','Отменить']:
		await message.answer('Пожалуйста, подтведите или отмените заказ, используя клавиатуру ниже:')
		return
	await state.update_data(confirm_status=message.text)
	if message.text == 'Подтвердить':
		await state.finish()
	elif message.text == 'Отменить':
		await state.finish()
		
def register_handlers_order(dp: Dispatcher):
	dp.register_message_handler(order_start, commands="order", state="*")
	dp.register_message_handler(order_start, Text(equals='Оформить заказ', ignore_case=True), state="*")
	dp.register_message_handler(clothes_chosen, state=OrderClothes.waiting_for_clothes_url)
	dp.register_message_handler(color_chosen, state=OrderClothes.waiting_for_clothes_color)
	dp.register_message_handler(size_order, state=OrderClothes.waiting_for_clothes_size)
	dp.register_message_handler(confirm_order, state=OrderClothes.waiting_for_confirm)

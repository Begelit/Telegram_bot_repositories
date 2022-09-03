from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from handlers.parserANDdb import parser 
import asyncio
from selenium import webdriver
import time
import json
from datetime import datetime

lock = asyncio.Lock()

bot = Bot(token='5503862888:AAE4i04YESiyI49I9PCzsWpy2SWNvGDFixA')

class OrderClothes(StatesGroup):
	waiting_for_clothes_url = State()
	waiting_for_clothes_color = State()
	waiting_for_clothes_size = State()
	waiting_for_confirm = State()

async def order_start(message: types.Message, state: FSMContext):
	#print(message['message_id'])
	#print(message.chat.id)
	await bot.delete_message(message.chat.id,message['message_id'])
	msg = await message.answer("Пожалуйста, отправьте ссылку, ведущую на товар.")
	async with state.proxy() as data:
		data['msgs_id'] = dict()
		data['msgs_id']['send_url_msg_id'] = msg['message_id']
	await OrderClothes.waiting_for_clothes_url.set()

async def clothes_chosen(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		send_url_msg_id = data['msgs_id']['send_url_msg_id']
	#await message.answer("Пожалуйста, подождите.")

	#url = message.text

	#driver_path = '/home/koza/Reps/drivers/chromedriver'
	#driver = parser.start_driverSession(driver_path=driver_path)
	
	async with lock:
	
		await bot.delete_message(message.chat.id,send_url_msg_id)
		
		wait_msg = await message.answer("Пожалуйста, подождите.")

		url = message.text

		driver_path = '/home/koza/Reps/drivers/chromedriver'
		driver = parser.start_driverSession(driver_path=driver_path)
		
		status,driver = parser.get_page_source(driver,url)
		#await asyncio.sleep(3)
		
	if status == False:
		driver.close()
		await asyncio.sleep(1)
		driver.quit()
		await asyncio.sleep(3)
		await bot.delete_message(message.chat.id,wait_msg['message_id'])
		await bot.delete_message(message.chat.id,message['message_id'])
		uncorrect_msg = await message.answer("Ссылка некорректна. Попробуйте ещё раз")
		async with state.proxy() as data:
			data['msgs_id']['send_url_msg_id'] = uncorrect_msg['message_id']
		return
		
	status,product_info = parser.get_product_info(driver)
	
	if status == 'have not clothes':
		driver.close()
		await asyncio.sleep(1)
		driver.quit()
		await asyncio.sleep(3)
		
		await bot.delete_message(message.chat.id,wait_msg['message_id'])
		await bot.delete_message(message.chat.id,message['message_id'])
		
		uncorrect_msg = await message.answer("Товар по этой ссылке не обнаружен. Попробуйте снова.")
		
		async with state.proxy() as data:
			data['msgs_id']['send_url_msg_id'] = uncorrect_msg['message_id']
			
		return
	elif status == 'False':
		driver.close()
		await asyncio.sleep(1)
		driver.quit()
		await asyncio.sleep(3)
		
		await bot.delete_message(message.chat.id,wait_msg['message_id'])
		await bot.delete_message(message.chat.id,message['message_id'])
		
		uncorrect_msg = await message.answer("Что-то пошло не так... Попробуйте ещё раз")
		
		async with state.proxy() as data:
			data['msgs_id']['send_url_msg_id'] = uncorrect_msg['message_id']
			
		return
		
	driver.close()
	await asyncio.sleep(1)
	driver.quit()
	
	async with state.proxy() as data:
		data['productDetail'] = product_info
		#data['login_link'] = login_link
		data['received_url'] = message.text
		
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for color in product_info['color']:
		keyboard.add(color)
		
	await bot.delete_message(message.chat.id,wait_msg['message_id'])
	#await bot.delete_message(message.chat.id,message['message_id'])
	
	color_buttons_msg = await message.answer("Укажите нужный цвет:", reply_markup=keyboard)
	
	async with state.proxy() as data:
		data['msgs_id']['color_buttons_msg_id'] = color_buttons_msg['message_id']
		data['msgs_id']['url_msg_id'] = message['message_id']
		
	await OrderClothes.waiting_for_clothes_color.set()
	
async def color_chosen(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		color_buttons_msg_id = data['msgs_id']['color_buttons_msg_id']
		order_data = data
	#print(order_data)
	
	colors_list = [color for color in order_data['productDetail']['color']]
	if message.text not in colors_list:
	
		await bot.delete_message(message.chat.id,color_buttons_msg_id)
		await bot.delete_message(message.chat.id,message['message_id'])
		
		color_buttons_msg = await message.answer('Пожалуйста, введите нужный цвет, используя клавиатуру ниже:')
		
		async with state.proxy() as data:
			data['msgs_id']['color_buttons_msg_id'] = color_buttons_msg['message_id']
			
		return
		
	async with state.proxy() as data:
		data['received_color'] = message.text
	#await state.update_data(received_color=message.text)
	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	#print(order_data)
	for size in order_data['productDetail']['color'][message.text]['size']:
		keyboard.add(size)
		
	await bot.delete_message(message.chat.id,color_buttons_msg_id)
	
	size_button_msg = await message.answer("Теперь выберите размер:", reply_markup=keyboard)
	
	async with state.proxy() as data:
		data['msgs_id']['size_button_msg_id'] = size_button_msg['message_id']
		
	await OrderClothes.waiting_for_clothes_size.set()
	
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
	#print(order_data)
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
		await message.answer('Пожалуйста, подтведите или отмените заказ, используя клавиатуру ниже и в выпадающем меню справа:')
		return
	async with state.proxy() as data:
		data['confirm_status'] = message.text
		data['username'] = message.from_user.username
		data['datetime'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
		#driver_url = data['driver_url']
		#driver_session_id = data['driver_session_id']
		order_data = data
		json_dict = dict()
		for key in data:
			json_dict[key] = data[key]
		#print(json_dict)
		#json_file = open('clothe_data.json','w')
		#json.dump(json_dict,json_file,indent=6)
		#json_file.close()

	#time.sleep(4)
	#new_driver = webdriver.Remote(command_executor = driver_url, desired_capabilities={})
	#new_driver.close()
	#new_driver.session_id = driver_session_id
	#await state.update_data(confirm_status=message.text)
	if message.text == 'Подтвердить':
		print(json_dict)
		json_file = open('clothe_data.json','w')
		json.dump(json_dict,json_file,indent=6)
		json_file.close()
		print(message.entities)
		#url = order_data['received_url']
		#driver_path = '/home/koza/Reps/drivers/chromedriver'
		#driver = parser.start_driverSession(driver_path=driver_path)
		#login_link = order_data['login_link']
		#print(order_data)
		####<<<<ТИПА ФОРМИРУЕМ КОРЗИНУ########################################
		'''
		#login_link,driver = parser.get_login_link(driver)
		print(login_link)
		if login_link != True:
			async with lock:
				driver = parser.get_page_source(driver,login_link)
				await asyncio.sleep(3)
			async with lock:
				driver = parser.login_user(driver)
				await asyncio.sleep(3)
			async with lock:
				driver = parser.get_page_source(driver,url)
				await asyncio.sleep(3)
		else:
			async with lock:
				driver = parser.get_page_source(driver,url)
				await asyncio.sleep(3)
		parser.create_basket(order_data,driver)
		'''
		####ТИПА ФОРМИРУЕМ КОРЗИНУ>>>>########################################
		
		print('\nmay be done...')
		#driver.close()
		#await asyncio.sleep(1)
		#driver.quit()
		
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

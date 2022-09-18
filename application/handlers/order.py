from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from handlers.parserANDdb import parser
from handlers.database import requests_database
import asyncio
from selenium import webdriver
import time
import json
from datetime import datetime
import os

lock = asyncio.Lock()

bot = Bot(token='5687809554:AAEMnikAnpF5FfHb6dX78Uw-cSshOf1BD0s')

class OrderClothes(StatesGroup):
	waiting_for_clothes_url = State()
	waiting_for_clothes_color = State()
	waiting_for_clothes_size = State()
	waiting_for_confirm = State()
	ignore_msg = State()
	start_st = State()
	order_start_state = State()
	amount_state = State()
	change_order_list_state = State()
	delete_order_state = State()
	admin_menu_state = State()
	get_order_info_admin_state = State()
	
async def start(message: types.Message, state: FSMContext):
	await state.finish()
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Начать!", callback_data="/start_order"))
	await message.answer('Привет! Добро пожаловать в менеджер заказов предметов одежды. Чтобы приступить нажми "Начать!".',reply_markup=keyboard)
	await OrderClothes.start_st.set()
	
async def cmd_start(call: types.CallbackQuery, state: FSMContext):
	#if message.text == '/start_order' or message.text == 'Начать!':
	if call.data == '/start_order':
		'''
		async with state.proxy() as data:
			if 'post_start_msgs_id' in data:
				try:
				
					await bot.delete_message(call.message.chat.id,data['post_start_msgs_id'])
				except:
					pass
		'''
		await state.finish()
		
		user_access = requests_database.get_username_status(call.from_user.username)
		
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Оформить заказ", callback_data="/order"))
		keyboard.add(types.InlineKeyboardButton(text="Список заказов", callback_data="/all_orders"))
		if user_access == 'admin':
			keyboard.add(types.InlineKeyboardButton(text="Меню администратора", callback_data="/admin"))
		keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="/cancel"))

		msg = await call.message.edit_text('Чтобы оставить заявку, пожалуйста, нажмите "Оформить заказ". Чтобы посмотреть все свои заказы нажмите "Список заказов".',reply_markup=keyboard)
		await call.answer()
		
		async with state.proxy() as data:
			#data['msgs_id'] = dict()
			data['start_msgs_id'] = msg['message_id']
			
		await OrderClothes.order_start_state.set()


async def order_start(call: types.CallbackQuery, state: FSMContext):

	if call.data == '/order':	

		msg = await call.message.edit_text('Пожалуйста, отправьте ссылку, ведущую на товар. Нажми /cancel если хочешь отменить  действие.')
		await call.answer()
		async with state.proxy() as data:
			data['msgs_id'] = dict()
			data['msgs_id']['send_url_msg_id'] = msg['message_id']
		await OrderClothes.waiting_for_clothes_url.set()
	elif call.data == '/cancel':
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		await call.answer()
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	elif call.data == '/all_orders':
		async with state.proxy() as data:
			await bot.delete_message(call.message.chat.id,data['start_msgs_id'])
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data="/cancel"))
		msg = await call.message.answer('Ваш список заказов:',reply_markup=keyboard)
		await call.answer()
		orders_data_dict = requests_database.get_info_order_user(call.from_user.username)
		
		async with state.proxy() as data:
			data['msgs_id'] = dict()
			data['msgs_id']['order_list'] = dict()
			data['msgs_id']['order_list']['firstMsg_ordlist_id'] = msg['message_id']
			data['orders_data_dict'] = orders_data_dict
			
		for index in range(len(orders_data_dict)):
		
			keyboard = types.InlineKeyboardMarkup()
			#keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="/delete_{}_{}".format(str(orders_data_dict[str(index)]['order_id']),str(index))))
			
			order_data_dict_index = orders_data_dict[str(index)]
			
			if order_data_dict_index['order_status'] == 'handling':
				status = 'Заявка обрабатывается'
				keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="/delete_{}_{}".format(str(orders_data_dict[str(index)]['order_id']),str(index))))
			elif order_data_dict_index['order_status'] == 'payed':
				status = 'Заявка оплачена'
			
			answer = f'''{str(index+1)}) {order_data_dict_index["order_item_name"]}
			    URL:[{order_data_dict_index["order_item_url"]}]
			    
			    id заказа: {order_data_dict_index["order_id"]}
			    
			    Цвет: {order_data_dict_index["order_item_color"]}
			    Размер: {order_data_dict_index["order_item_size"]}
			    Количество: {order_data_dict_index["order_item_amount"]}
			    Стоимость: {order_data_dict_index["order_total_price"]} {order_data_dict_index["order_item_currency"]}
			    Дата поступления заявки: {order_data_dict_index["order_creating_date"]}
			'''
			msg = await call.message.answer(
				answer,reply_markup=keyboard,disable_web_page_preview=True
				)
			async with state.proxy() as data:
				data['msgs_id']['order_list'][str(orders_data_dict[str(index)]['order_id'])] = msg['message_id']

		await OrderClothes.change_order_list_state.set()
		
	elif call.data == '/admin':
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Выгрузить таблицу заказов", callback_data="/table"))
		keyboard.add(types.InlineKeyboardButton(text="Изменить статус заказа", callback_data="/change_status"))
		keyboard.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data="/cancel"))
		msg = await call.message.edit_text('Добро пожаловать в меня администратора, пожалуйста, выбери необходимое действие.',reply_markup=keyboard)
		await call.answer()
		await OrderClothes.admin_menu_state.set()
		
async def admin_menu(call: types.CallbackQuery, state: FSMContext):
	if call.data == '/cancel':
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Нажми на "Меню" для продолжения.',reply_markup=keyboard)
		await call.answer()
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	elif call.data == '/table':
		requests_database.get_orders_document()
		open_xlsx = open('/home/koza/Reps/shein_bot/application/handlers/database/orders.xlsx','rb')
		await bot.send_document(call.from_user.id,open_xlsx)
		await OrderClothes.admin_menu_state.set()
	elif call.data == '/change_status':
		msg = await call.message.edit_text('Отправь номер id заявки.')
		async with state.proxy() as data:
			data['send_order_id_message'] = msg['message_id']
		await OrderClothes.get_order_info_admin_state.set()
		
async def get_order_info_admin(message: types.Message, state: FSMContext):
	await bot.delete_message(message.chat.id,message['message_id'])
	async with state.proxy() as data:
		await bot.delete_message(message.chat.id,data['send_order_id_message'])
	dick_order = requests_database.get_info_order_user_admin(message.text)
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Отмена", callback_data="/cancel"))
	if dick_order['order_status'] == 'handling':
		status = 'Заявка обрабатывается'
		keyboard.add(types.InlineKeyboardButton(text="Оплачено", callback_data="/payed"))
	elif dick_order['order_status'] == 'deleted':
		status = 'Заявка удалена пользователем'
	elif dick_order['order_status'] == 'payed':
		status = 'Заявка оплачена'
	answer_msg = f''' {dick_order["order_item_name"]}
    URL:[{dick_order["order_item_url"]}]
    
    id заказа: {dick_order["order_id"]}
    
    Цвет: {dick_order["order_item_color"]}
    Размер: {dick_order["order_item_size"]}
    Количество: {dick_order["order_item_amount"]}
    Стоимость: {dick_order["order_total_price"]} {dick_order["order_item_currency"]}
    Дата поступления заявки: {dick_order["order_creating_date"]}
    Статус: {status}
'''
	msg = await message.answer(answer_msg,reply_markup=keyboard,disable_web_page_preview=True)
	
async def change_order_list(call: types.CallbackQuery, state: FSMContext):
	if call.data == '/cancel':
		async with state.proxy() as data:
			for key in data['msgs_id']['order_list']:
				await bot.delete_message(call.message.chat.id,data['msgs_id']['order_list'][key])
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.answer('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	elif 'delete' in call.data:
		del_key = call.data.split('_')[1]
		index = call.data.split('_')[2]
		async with state.proxy() as data:
			for key in data['msgs_id']['order_list']:
				if key != del_key:
					await bot.delete_message(call.message.chat.id,data['msgs_id']['order_list'][key])
			
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="/delete_{}".format(str(del_key))))
			keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="/cancel".format(str(del_key))))
			order_data_dict_index = data['orders_data_dict'][index]
			answer = f''' {order_data_dict_index["order_item_name"]}
			    URL:[{order_data_dict_index["order_item_url"]}]
			    
			    id заказа: {order_data_dict_index["order_id"]}
			    
			    Цвет: {order_data_dict_index["order_item_color"]}
			    Размер: {order_data_dict_index["order_item_size"]}
			    Количество: {order_data_dict_index["order_item_amount"]}
			    Стоимость: {order_data_dict_index["order_total_price"]} {order_data_dict_index["order_item_currency"]}
			    Дата поступления заявки: {order_data_dict_index["order_creating_date"]}
			'''
			msg = await call.message.edit_text(answer+'\n\nВЫ ТОЧНО СОБИРАЕТЕСЬ УДАЛИТЬ ЗАКАЗ?',reply_markup=keyboard,disable_web_page_preview=True)
		await OrderClothes.delete_order_state.set()
		
async def delete_order(call: types.CallbackQuery, state: FSMContext):
	if call.data == '/cancel':
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	elif 'delete' in call.data:
		await state.finish()
		del_key = call.data.split('_')[1]
		requests_database.delete_order(del_key)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Заказ удалён, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
		
async def clothes_chosen(message: types.Message, state: FSMContext):
	
	#async with lock:
	if message.text == '/cancel':
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['msgs_id']['send_url_msg_id'])

		await state.finish()
		
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await message.answer('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		#await call.answer()
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	else:
		await OrderClothes.ignore_msg.set()
	
		async with state.proxy() as data:
			send_url_msg_id = data['msgs_id']['send_url_msg_id']
	
		await bot.delete_message(message.chat.id,send_url_msg_id)
		
		wait_msg = await message.answer("Пожалуйста, подождите.",reply_markup=types.ReplyKeyboardRemove())

		url = message.text

		driver_path = '/home/koza/Reps/drivers/chromedriver'
		driver = parser.start_driverSession(driver_path=driver_path)
		
		status,driver = parser.get_page_source(driver,url)
		
		if status == False:
			driver.close()
			await asyncio.sleep(1)
			driver.quit()
			await asyncio.sleep(3)
			await bot.delete_message(message.chat.id,wait_msg['message_id'])
			await bot.delete_message(message.chat.id,message['message_id'])
			uncorrect_msg = await message.answer("Ссылка некорректна. Попробуйте ещё раз отправить ссылку. Либо отмените действие нажав на /cancel",reply_markup=types.ReplyKeyboardRemove())
			await OrderClothes.waiting_for_clothes_url.set()
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
			
			uncorrect_msg = await message.answer("Товар по этой ссылке не обнаружен или произошел сбой. Попробуйте снова отправить ссылку. Либо отмените действие нажав на /cancel",reply_markup=types.ReplyKeyboardRemove())
			await OrderClothes.waiting_for_clothes_url.set()
			async with state.proxy() as data:
				data['msgs_id']['send_url_msg_id'] = uncorrect_msg['message_id']
			
			return
		elif status == False:
			driver.close()
			await asyncio.sleep(1)
			driver.quit()
			await asyncio.sleep(3)
			
			await bot.delete_message(message.chat.id,wait_msg['message_id'])
			await bot.delete_message(message.chat.id,message['message_id'])
			
			uncorrect_msg = await message.answer("Что-то пошло не так... Попробуйте ещё раз отправить ссылку. Либо отмените действие нажав на /cancel",reply_markup=types.ReplyKeyboardRemove())
			await OrderClothes.waiting_for_clothes_url.set()
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
			
		keyboard = types.InlineKeyboardMarkup()
		for color in product_info['color']:
			keyboard.add(types.InlineKeyboardButton(text=color, callback_data=color))
			
		keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='/cancel'))
			
		await bot.delete_message(message.chat.id,wait_msg['message_id'])
		
		color_buttons_msg = await message.answer("Укажите нужный цвет:", reply_markup=keyboard)
		
		async with state.proxy() as data:
			data['msgs_id']['color_buttons_msg_id'] = color_buttons_msg['message_id']
			data['msgs_id']['url_msg_id'] = message['message_id']
			
		await OrderClothes.waiting_for_clothes_color.set()
	
async def ignoreMsg_whileScrap(message: types.Message, state: FSMContext):
	await bot.delete_message(message.chat.id,message['message_id'])
	
async def color_chosen(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		color_buttons_msg_id = data['msgs_id']['color_buttons_msg_id']
		url_id = data['msgs_id']['url_msg_id']
		order_data = data

	if call.data == '/cancel':

		await bot.delete_message(call.message.chat.id,url_id)
		await state.finish()
		
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		await call.answer()	
		
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	else:
			
		async with state.proxy() as data:
			data['received_color'] = call.data
		if order_data['productDetail']['color'][call.data]['size'] == 'single_size':
			#await bot.delete_message(call.message.chat.id,color_buttons_msg_id)
			async with state.proxy() as data:
				data['received_size'] = 'Нет размера'
			msg = await call.message.edit_text('Пожалуйста, укажите необходимое количество товара. Если хотите отменить действие, нажмите /cancel.')
			async with state.proxy() as data:
				data['msgs_id']['send_amount_msg_id'] = msg['message_id']
			await OrderClothes.amount_state.set()
		else:
			
			keyboard = types.InlineKeyboardMarkup()
			for size in order_data['productDetail']['color'][call.data]['size']:
				keyboard.add(types.InlineKeyboardButton(text=size, callback_data=size))
			keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='/cancel'))
			
			size_button_msg = await call.message.edit_text("Теперь выберите размер:", reply_markup=keyboard)
			
			await call.answer()
			
			async with state.proxy() as data:
				data['msgs_id']['size_button_msg_id'] = size_button_msg['message_id']
				
			await OrderClothes.waiting_for_clothes_size.set()
		
async def size_order(call: types.CallbackQuery, state: FSMContext):

	async with state.proxy() as data:
		order_data = data
		size_button_msg_id = data['msgs_id']['size_button_msg_id']
		url_id = data['msgs_id']['url_msg_id']
	if call.data == '/cancel':
		await bot.delete_message(call.message.chat.id,url_id)
		await state.finish()
		
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		await call.answer()
		
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	else:

		async with state.proxy() as data:
			data['received_size'] = call.data
		msg = await call.message.edit_text('Пожалуйста, укажите необходимое количество товара. Если хотите отменить действие, нажмите /cancel.')
		async with state.proxy() as data:
			data['msgs_id']['send_amount_msg_id'] = msg['message_id']
		await OrderClothes.amount_state.set()
		
async def amount_clothes_order(message: types.Message, state: FSMContext):
	if message.text == '/cancel':
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['msgs_id']['send_amount_msg_id'])
			await bot.delete_message(message.chat.id,data['msgs_id']['url_msg_id'])
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await message.answer('Действие отменено, нажми на "Меню" для продолжения.',reply_markup=keyboard)
		#await call.answer()
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	elif message.text.isdigit() == False:
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['msgs_id']['send_amount_msg_id'])
		msg = await message.answer('Пожалуйста, введите корректное значение, чтобы указать количество товара. Если хотите отменить действие, нажмите /cancel.')
		async with state.proxy() as data:
			data['msgs_id']['send_amount_msg_id'] = msg['message_id']
		return
	elif (message.text.isdigit() == True) and (int(message.text) >= 100):
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['msgs_id']['send_amount_msg_id'])
		msg = await message.answer('Слишком большое значение, укажите меньшее значение. Если хотите отменить действие, нажмите /cancel.')
		async with state.proxy() as data:
			data['msgs_id']['send_amount_msg_id'] = msg['message_id']
		return
	else:
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['msgs_id']['send_amount_msg_id'])
		async with state.proxy() as data:
			data['received_amount'] = message.text
			order_data = data
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="/confirm"))
		keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="/cancel"))
		order_data_msg = await message.answer("Почти готово! Ваш заказ:"
					f"\n\n  {order_data['productDetail']['name']}"
					f"\n    Цвет: {order_data['received_color']}"
					f"\n    Размер: {order_data['received_size']}"
					f"\n    Количество: {order_data['received_amount']}"
					f"\n    Цена: {str(float(order_data['productDetail']['color'][order_data['received_color']]['price'])*int(order_data['received_amount']))}"f" {order_data['productDetail']['color'][order_data['received_color']]['currency']}"
					,reply_markup=keyboard)
		#await call.answer()
		async with state.proxy() as data:
			data['msgs_id']['order_data_msg_id'] = order_data_msg['message_id']
			data['total_price'] = float(order_data['productDetail']['color'][order_data['received_color']]['price'])*int(order_data['received_amount'])
			data['currency'] = order_data['productDetail']['color'][order_data['received_color']]['currency']
		await OrderClothes.waiting_for_confirm.set()
		
		
async def confirm_order(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		order_data_msg_id = data['msgs_id']['order_data_msg_id']
		url_msg_id = data['msgs_id']['url_msg_id']
	if call.data == '/cancel':
		await bot.delete_message(call.message.chat.id,url_msg_id)
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
		msg = await call.message.edit_text('Действие отменено, нажмите "Меню" для продолжения.',reply_markup=keyboard)
		await call.answer()
		async with state.proxy() as data:
			data['post_start_msgs_id'] = msg['message_id']
		await OrderClothes.start_st.set()
	else:

		async with state.proxy() as data:
			data['confirm_status'] = 'Confirm' if call.data == '/confirm' else False
			data['username'] = call.from_user.username
			data['datetime'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
			order_data = data
			json_dict = dict()
			for key in data:
				json_dict[key] = data[key]

		if call.data == '/confirm':
			async with lock:
				requests_database.create_order(json_dict)
				index_json = len(os.listdir('./json_data'))
				json_file = open('./json_data/clothe_data_{}.json'.format(str(index_json)),'w')
				json.dump(json_dict,json_file,indent=6)
				json_file.close()
			await bot.delete_message(call.message.chat.id,url_msg_id)
			
			await state.finish()
			
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data="/start_order"))
			msg = await call.message.edit_text('Заявка создана! Нажмите "Меню" для продолжения.',reply_markup=keyboard)
			await call.answer()
			
			async with state.proxy() as data:
				data['post_start_msgs_id'] = msg['message_id']
				
			await OrderClothes.start_st.set()
		
def register_handlers_order(dp: Dispatcher):
	#dp.register_message_handler(cmd_start, commands="start", state=OrderClothes.start_st)
	#dp.register_message_handler(cmd_start, commands="start", state='*')
	dp.register_message_handler(start,commands='start', state='*')
	
	#dp.register_message_handler(cmd_start, state=OrderClothes.start_st)
	dp.register_callback_query_handler(cmd_start, state=OrderClothes.start_st)
	
	dp.register_callback_query_handler(change_order_list, state=OrderClothes.change_order_list_state)
	
	dp.register_callback_query_handler(delete_order, state=OrderClothes.delete_order_state)
	
	dp.register_callback_query_handler(admin_menu,state=OrderClothes.admin_menu_state)
	
	dp.register_message_handler(get_order_info_admin,state=OrderClothes.get_order_info_admin_state)
	
	#dp.register_message_handler(order_start, commands="order", state="*")
	#dp.register_message_handler(order_start, Text(equals='Оформить заказ', ignore_case=True), state="*")
	#dp.register_message_handler(order_start, commands="order", state=OrderClothes.order_start_state)
	#dp.register_message_handler(order_start, Text(equals='Оформить заказ', ignore_case=True), state=OrderClothes.order_start_state)
	#dp.register_message_handler(order_start, state=OrderClothes.order_start_state)
	dp.register_callback_query_handler(order_start, state=OrderClothes.order_start_state)
	
	dp.register_message_handler(clothes_chosen, state=OrderClothes.waiting_for_clothes_url)
	
	#dp.register_message_handler(color_chosen, state=OrderClothes.waiting_for_clothes_color)
	dp.register_callback_query_handler(color_chosen, state=OrderClothes.waiting_for_clothes_color)
	
	#dp.register_message_handler(size_order, state=OrderClothes.waiting_for_clothes_size)
	dp.register_callback_query_handler(size_order, state=OrderClothes.waiting_for_clothes_size)
	
	dp.register_message_handler(amount_clothes_order, state=OrderClothes.amount_state)
	
	#dp.register_message_handler(confirm_order, state=OrderClothes.waiting_for_confirm)
	dp.register_callback_query_handler(confirm_order, state=OrderClothes.waiting_for_confirm)
	
	dp.register_message_handler(ignoreMsg_whileScrap, state=OrderClothes.ignore_msg)

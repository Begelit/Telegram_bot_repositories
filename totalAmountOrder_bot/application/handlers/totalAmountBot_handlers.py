from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import asyncio
from selenium import webdriver
import time
import json
from datetime import datetime
import os
import configparser

config = configparser.ConfigParser()
config.read('/home/koza/Reps/totalAmountCalculator_rep/application/token.ini')
bot = Bot(token=config.get('token', 'bot_token'))

class TotalAmount(StatesGroup):
	select_market_state = State()
	send_amount_clothe_state = State()
	amount_handling_state = State()

async def start(message: types.Message, state: FSMContext):
	await state.finish()
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Начать!", callback_data="/start_amount"))
	await message.answer('Привет! Добро пожаловать в калькулятор корзины. Чтобы приступить нажми "Начать!".',reply_markup=keyboard)
	await TotalAmount.select_market_state.set()

async def select_market(call: types.CallbackQuery, state: FSMContext):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Shein", callback_data="/Shein"))
	keyboard.add(types.InlineKeyboardButton(text="ZARA", callback_data="/ZARA"))
	keyboard.add(types.InlineKeyboardButton(text="Lichi", callback_data="/Lichi"))
	keyboard.add(types.InlineKeyboardButton(text="Next", callback_data="/Next"))
	keyboard.add(types.InlineKeyboardButton(text="Massimo Dutti", callback_data="/Massimo_Dutti"))
	await call.message.edit_text('Выберите магазин',reply_markup=keyboard)
	await call.answer()
	await TotalAmount.send_amount_clothe_state.set()
	
async def send_amount_clothe(call: types.CallbackQuery, state: FSMContext):
	if call.data == '/Shein':
		async with state.proxy() as data:
			data['currency'] = 'RUB'
			data['coef'] = 1.224
			data['shop'] = call.data.replace('/','')
		msg = await call.message.edit_text('Введите сумму товара(в рублях). Либо нажмите /cancel чтобы вернуться назад.')
		await call.answer()
	else:
		async with state.proxy() as data:
			data['currency'] = 'KZT'
			data['coef'] = 1.2/7
			data['shop'] = call.data.replace('/','')
		msg = await call.message.edit_text('Введите сумму товара(в тенге). Либо нажмите /cancel чтобы вернуться назад.')
		await call.answer()
	async with state.proxy() as data:
		data['amount_msg_id'] = msg['message_id']
	await TotalAmount.amount_handling_state.set()
		
async def amount_handling(message: types.Message, state: FSMContext):
	if message.text == '/cancel':
		async with state.proxy() as data:
			await bot.delete_message(message.chat.id,data['amount_msg_id'])
			await bot.delete_message(message.chat.id,message['message_id'])
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Начать!", callback_data="/start_amount"))
		await message.answer('Добро пожаловать в калькулятор корзины! Чтобы приступить нажми "Начать!".',reply_markup=keyboard)
		await TotalAmount.select_market_state.set()
	elif message.text.replace('.','',1).isdigit() == True:
		#print(message.text.replace('.','',1))
		#print(message.text.replace('.','',1).isdigit())
		if len(message.text) > 10:
			msg = await message.answer('Сумма слишком большая либо некорректна введена, попробуйте ещё раз. Если хотите завершить процесс нажмите /cancel .')
			async with state.proxy() as data:
				await bot.delete_message(message.chat.id,data['amount_msg_id'])
			await bot.delete_message(message.chat.id,message['message_id'])
			async with state.proxy() as data:
				data['amount_msg_id'] = msg['message_id']
			await TotalAmount.amount_handling_state.set()
		else:
			async with state.proxy() as data:
				currency = data['currency']
				coef = data['coef']
				shop = data['shop']
			msg = await message.answer(
						f'Магазин: {shop}'
						f'\n\n  Стоимость товара: {message.text} {currency}'
						f'\n\n  Итого к оплате: {str(round( float(message.text)*coef ))} RUB'
						f'\n\n Нажмите /start для продоллжения.')
	else:
		msg = await message.answer('Сумма некорректна, попробуйте ещё раз, либо вернитесь в меню отправив /cancel)')
		async with state.proxy() as data:
				await bot.delete_message(message.chat.id,data['amount_msg_id'])
		await bot.delete_message(message.chat.id,message['message_id'])
		async with state.proxy() as data:
			data['amount_msg_id'] = msg['message_id']
		await TotalAmount.amount_handling_state.set()
		#else:
			
			#async with state.proxy() as data:
				
				
			
	
def register_handlers_totalAmount(dp: Dispatcher):
	dp.register_message_handler(start,commands='start', state='*')
	dp.register_callback_query_handler(select_market, state=TotalAmount.select_market_state)
	dp.register_callback_query_handler(send_amount_clothe, state=TotalAmount.send_amount_clothe_state)
	dp.register_message_handler(amount_handling, state=TotalAmount.amount_handling_state)

import telebot
#from aiogram import Bot, Dispatcher, executer, types
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import test_Req
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import asyncio
import math

#logging.basicConfig()

bot = Bot(token='5415272308:AAFlMEbYITbzEqrOGDYDBhSfuJ0zE_2lCdQ')
dp = Dispatcher(bot)

def getProDet_dict(url):
	redUrl = test_Req.getRedirectedUrl(url)
	proDet_dict = test_Req.get_productDetail_dict(redUrl)
	return test_Req.get_mainInfo(proDet_dict)
	


@dp.message_handler()
async def echo(message: types.Message):
	totalAmount, response = test_Req.createResponse(message.text)
	for index in range(len(response)):
		name = response[str(index)]['name']
		url = response[str(index)]['url']
		size = response[str(index)]['size']
		amount = response[str(index)]['amount']
		if response[str(index)]['stock'] > 100:
			stock = 'В наличии'
		else :
			stock = response[str(index)]['stock']
		#need = response[str(index)]['need']
		#await message.answer('1) '+name+'\n\n'+url+'\n\n\tSize: '+size+'\n\tPrice: '+str(round(amount))+'\n\tStock: '+str(stock)+'\n\tNeed for quantity: '+str(need))
		await message.answer(str(index+1)+') '+name+'\n\n\tРазмер: '+size+'\n\tЦена: '+str(round(amount))+' руб.\n\tНа складе: '+str(stock)+'\n\n'+(u''+url).encode('utf-8'))
		#await message.answer(f"<a href = '"+url+"'></a>")
	await message.answer('\n\n\tОбщая сумма: '+str(math.floor(totalAmount))+' руб.')
	"""
	prodVar = getProDet_dict(message.text)
	print('\nfirst_url','\n',message.text,'\n')
	for size in prodVar:
		await message.answer(size+' price - '+str(prodVar[size]['amount']))
		await message.answer(size+' stock - '+str(prodVar[size]['stock']))
	"""
	
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates = True)

#bot = telebot.TeleBot('5503862888:AAFw2wDgevBr9FGOSpX0G5e6RJqMQSBEN4E')

#@bot.message_handler(content_types=['text'])
#def start(message):

"""
def getProDet_dict(url):
	redUrl = test_Req.getRedirectedUrl(url)
	proDet_dict = test_Req.get_productDetail_dict(redUrl)
	return test_Req.get_mainInfo(proDet_dict)

bot = telebot.TeleBot('5503862888:AAFw2wDgevBr9FGOSpX0G5e6RJqMQSBEN4E')

if __name__ == "__main__":
	#url = 'https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshother&localcountry=other&currency=RUB&id=10357731&url_from=GM7266541214465818624'
	bot = telebot.TeleBot('5503862888:AAFw2wDgevBr9FGOSpX0G5e6RJqMQSBEN4E')
	@bot.message_handler(content_types=['text'])
	def response(message):
		proDetVar = getProDet_dict(message)
		for size in proDetVar:
			#bot.send_message(message.from_user.id,str(size)+' price - '+proDetVar[str(size)])
			mes1 = size+' price - '+str(proDetVar[size]['amount'])
			mes2 = size+' stock - '+str(proDetVar[size]['stock'])
			bot.send_message(message.from_user.id,mes1)
			bot.send_message(message.from_user.id,mes2)
"""

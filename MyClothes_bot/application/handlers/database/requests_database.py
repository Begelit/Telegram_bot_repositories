from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from handlers.database.schema_database import User, Order
#from schema_database import User, Order
import configparser
import traceback
import json
import xlsxwriter
import os

def create_order(data):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)

		#s = session()
		#s.close()
		with session() as s:
		
			try:	
				username = data['username']
				num = None
				for num, row in enumerate(s.query(User).filter(User.user_username == username)):
					#print(row.user_username)
					user_pk_id = row.user_id
				if num == None:
					user_add = User(user_username = username)
					s.add(user_add)
					s.commit()
					for num, row in enumerate(s.query(User).filter(User.user_username == username)):
						user_pk_id = row.user_id
				
				order_add = Order(order_user_id = user_pk_id,
							order_item_name = data['productDetail']['name'],
							order_item_color = data['received_color'],
							order_item_size = data['received_size'],
							order_item_amount = data['received_amount'],
							order_total_price = data['total_price'],
							order_item_currency = data['currency'],
							order_item_url = data['received_url'],
							order_status = 'handling')
				s.add(order_add)
				s.commit()
				
			except:
				print(traceback.format_exc())
				return False
		return True
	except:
		print(traceback.format_exc())
		return False
		
def get_info_order_user(username):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		order_list = dict()
		
		with session() as s:
			try:
				for num, row in enumerate(s.query(User).filter(User.user_username == username)):
					user_pk_id = row.user_id
				num = 0
				for row in s.query(Order).filter(Order.order_user_id == user_pk_id):
					if row.order_status != 'deleted':
						order_list[str(num)] = dict()
						order_list[str(num)]['order_id'] = row.order_id
						order_list[str(num)]['order_user_id'] = row.order_user_id
						order_list[str(num)]['order_item_name'] = row.order_item_name
						order_list[str(num)]['order_item_color'] = row.order_item_color
						order_list[str(num)]['order_item_size'] = row.order_item_size
						order_list[str(num)]['order_item_amount'] = row.order_item_amount
						order_list[str(num)]['order_total_price'] = row.order_total_price
						order_list[str(num)]['order_item_currency'] = row.order_item_currency
						order_list[str(num)]['order_item_url'] = row.order_item_url
						order_list[str(num)]['order_status'] = row.order_status
						order_list[str(num)]['order_creating_date'] = str(row.order_creating_date)
						num +=1
					#print(order_list[str(num)])
				return order_list
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False

def delete_order(order_id_):
	try:
		
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		with session() as s:
			try:
				order = s.query(Order).filter(Order.order_id == int(order_id_)).one()
				order.order_status = 'deleted'
				s.commit()
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False
		
def get_username_status(username):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		with session() as s:
			try:
				for num, row in enumerate(s.query(User).filter(User.user_username == username)):
					user_access = row.user_access
				return user_access
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False

def get_orders_document():
	try:
		if os.path.exists('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/orders.xlsx') == True:
			os.remove('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/orders.xlsx')
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		with session() as s:
			try:
				workbook = xlsxwriter.Workbook('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/orders.xlsx')
				ws = workbook.add_worksheet()
				ws.write(0,0,'Дата')
				ws.write(0,1,'Имя пользователя')
				ws.write(0,2,'id Заявки')
				ws.write(0,3,'Название товара')
				ws.write(0,4,'Цвет')
				ws.write(0,5,'Размер')
				ws.write(0,6,'Количество')
				ws.write(0,7,'Стоимость')
				ws.write(0,8,'Валюта')
				ws.write(0,9,'Статус')
				ws.write(0,10,'Ссылка')
				for num, row in enumerate(s.query(Order).filter(Order.order_status != 'deleted')):
					ws.write(num+1,0,str(row.order_creating_date))
					for num_user, row_user in enumerate(s.query(User).filter(User.user_id == row.order_user_id)):
						ws.write(num+1,1,'@'+row_user.user_username)
					ws.write(num+1,2,row.order_id)
					ws.write(num+1,3,row.order_item_name)
					ws.write(num+1,4,row.order_item_color)
					ws.write(num+1,5,row.order_item_size)
					ws.write(num+1,6,row.order_item_amount)
					ws.write(num+1,7,row.order_total_price)
					ws.write(num+1,8,row.order_item_currency)
					ws.write(num+1,9,row.order_status)
					ws.write(num+1,10,row.order_item_url)
				workbook.close()
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False
		
def get_info_order_user_admin(order_id_):
	try:

		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		order = dict()
		
		with session() as s:
			try:
				#for num, row in enumerate(s.query(User).filter(User.user_username == username)):
				#	user_pk_id = row.user_id
				#num = 0
				for row in s.query(Order).filter(Order.order_id == order_id_):
					order = dict()
					order['order_id'] = row.order_id
					order['order_user_id'] = row.order_user_id
					order['order_item_name'] = row.order_item_name
					order['order_item_color'] = row.order_item_color
					order['order_item_size'] = row.order_item_size
					order['order_item_amount'] = row.order_item_amount
					order['order_total_price'] = row.order_total_price
					order['order_item_currency'] = row.order_item_currency
					order['order_item_url'] = row.order_item_url
					order['order_status'] = row.order_status
					order['order_creating_date'] = str(row.order_creating_date)
				return order
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False
		
def change_order_status_payed(order_id_):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

		user = config.get('mysql_login_data', 'usr')
		pswd = config.get('mysql_login_data', 'pswd')
		host = config.get('mysql_login_data', 'host')
		database = config.get('mysql_login_data', 'database')

		engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

		session = sessionmaker(bind = engine)
		
		order = dict()
		
		with session() as s:
			try:
				order = s.query(Order).filter(Order.order_id == int(order_id_)).one()
				order.order_status = 'payed'
				s.commit()
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False
		
#print(s.query(User).filter(User.user_username == 'user_test'))

#if __name__ == "__main__":
	#get_orders_document()
	#json_file = open('/home/koza/Reps/shein_bot/application/json_data/clothe_data_2.json')
	#order_data = json.load(json_file)
	#create_order(order_data)
	#get_info_order_user('dimchxn')
	#delete_order('3')

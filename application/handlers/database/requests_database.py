from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schema_database import User, Order
import configparser
import traceback
import json

def create_order(data):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/shein_bot/application/handlers/database/db_login_data.ini')

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
		config.read('/home/koza/Reps/shein_bot/application/handlers/database/db_login_data.ini')

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
				for num, row in enumerate(s.query(Order).filter(Order.order_user_id == user_pk_id)):
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
					#print(order_list[str(num)])
				return order_list
			except:
				print(traceback.format_exc())
				return False
	except:
		print(traceback.format_exc())
		return False

#print(s.query(User).filter(User.user_username == 'user_test'))

if __name__ == "__main__":
	json_file = open('/home/koza/Reps/shein_bot/application/json_data/clothe_data_2.json')
	order_data = json.load(json_file)
	create_order(order_data)
	#get_info_order_user('dimchxn')
	
	

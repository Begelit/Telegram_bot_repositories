from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schema_database import User, Order
import configparser
import traceback
import json

def create_order(data):
	try:
		config = configparser.ConfigParser()
		config.read('/home/koza/Reps/shein_bot/database/db_login_data.ini')

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
				#else:
				#	print([row.user_username for row in s.query(User.user_username).filter(User.user_id == user_pk_id)][0])
				order_add = Order(order_user_id = user_pk_id,
							order_item_name = data['productDetail']['name'],
							order_item_color = data['received_color'],
							order_item_size = data['received_size'],
							order_item_url = data['received_url'],
							order_status = 'handling')
				s.add(order_add)
				s.commit()
			except:
				print(traceback.format_exc())
	except:
		print(traceback.format_exc())

#print(s.query(User).filter(User.user_username == 'user_test'))

if __name__ == "__main__":
	json_file = open('/home/koza/Reps/shein_bot/application/json_data/clothe_data_3.json')
	order_data = json.load(json_file)
	create_order(order_data)

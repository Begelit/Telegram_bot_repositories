from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import configparser

config = configparser.ConfigParser()
config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

user = config.get('mysql_login_data', 'usr')
pswd = config.get('mysql_login_data', 'pswd')
host = config.get('mysql_login_data', 'host')
database = config.get('mysql_login_data', 'database')

engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host,database))

Base = declarative_base()

class User(Base):

	__tablename__ = 'Users'
	
	user_id = Column(Integer, primary_key=True)
	user_username = Column(String(50), nullable=False)
	user_access = Column(String(50), default = 'default', nullable=False)
	Order = relationship('Order')
	
class Order(Base):

	__tablename__ = 'Orders'
	
	order_id = Column(Integer, primary_key = True)
	order_user_id = Column(Integer, ForeignKey('Users.user_id'),nullable=False)
	
	order_item_name = Column(String(100), nullable = False)
	order_item_color = Column(String(50), nullable = False)
	order_item_size = Column(String(50), nullable = False)
	order_item_amount = Column(Integer, nullable = False)
	order_total_price = Column(Float, nullable = False)
	order_item_currency = Column(String(10), nullable = False)
	order_item_url = Column(String(500), nullable = False)
	
	#order_item_id = Column(Integer, ForeignKey('Items.item_id'),nullable=False)
	order_status = Column(String(50), nullable=False)
	order_creating_date = Column(DateTime, default = datetime.datetime.utcnow, nullable = False)
	
	User = relationship('User')
	#Item = relationship('Item')
'''	
class Item(Base):

	__tablename__ = 'Items'
	
	item_id = Column(Integer, primary_key = True)
	item_name = Column(String(100), nullable = False)
	item_color = Column(String(50), nullable = False)
	item_size = Column(String(50), nullable = False)
	item_url = Column(String(500), nullable = False)
	
	Order = relationship('Order')
'''
	
Base.metadata.create_all(engine)


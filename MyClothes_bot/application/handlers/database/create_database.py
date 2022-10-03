from sqlalchemy import create_engine
import configparser

config = configparser.ConfigParser()
config.read('/home/koza/Reps/Telegram_bot_repositories/MyClothes_bot/application/handlers/database/db_login_data.ini')

user = config.get('mysql_login_data', 'usr')
pswd = config.get('mysql_login_data', 'pswd')
host = config.get('mysql_login_data', 'host')
database = config.get('mysql_login_data', 'database')

mysql_engine = create_engine('mysql://{0}:{1}@{2}'.format(user, pswd, host))

existing_databases = mysql_engine.execute("SHOW DATABASES;")

existing_databases = [d[0] for d in existing_databases]
if database not in existing_databases:
	mysql_engine.execute("CREATE DATABASE {0}".format(database))
	print("Created database {0}".format(database))
else:
	print('DB is already exists.')

db_engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pswd, host, database))

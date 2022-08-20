from rethinkdb import RethinkDB
def pyAiRethinkDB_Create(name = str(),user_password = str()):
	r = RethinkDB()
	with r.connect(host='localhost',port=28015,user='admin',db='rethinkdb').repl() as conn:
		db_table_user = r.db('rethinkdb').table('users').run()
		usrs_list = [user['id'] for user in db_table_user]
		if (name in usrs_list) == False:
			r.db('rethinkdb').table('users').insert({'id':name, 'password': user_password}).run()
		else:
			print('\n '+name+' user is already created\n')
	with r.connect(host='localhost',port=28015,user=name,password=user_password).repl() as conn:
		db_list = r.db_list().run()
		if (name in db_list) == False:
			r.db_create(name).run()
			r.db(name).table_create(name).run(conn)
		else:
			print('\n '+name+' database is already created\n')
def deleteDB():
	r = RethinkDB()
	#with r.connect(host='localhost',port=28015,user='aiogram',password='aiogram_secret').repl() as conn:
	with r.connect(host='localhost',port=28015,user='admin',db='rethinkdb').repl() as conn:
		#r.db_create('aiogram').run()
		#r.db('aiogram').grant('aiogram', {'read': True, 'write': True}).run()
		#r.db('aiogram').table_create('aiogram').run()
		db_list = r.db('aiogram').table_list().run()
		print(db_list)
	"""
	with r.connect(host='localhost',port=28015,user='admin',db='rethinkdb').repl() as conn:
		#db_table_user = r.db('rethinkdb').table('users').run()
		#r.db_drop('aiogram').run()
		#db_list = r.db_list().run()
		table_list = r.table_list().run()
		print(table_list)
	"""
if __name__ == "__main__":
	#pyAiRethinkDB_Create(name = 'aiogram',user_password = 'aiogram_secret')
	deleteDB()

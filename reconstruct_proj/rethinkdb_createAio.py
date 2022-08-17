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
if __name__ == "__main__":
	pyAiRethinkDB_Create(name = 'aiogram',user_password = 'aiogram_secret')

rom rethinkdb import RethinkDB

def createDB():
        r = RethinkDB()
        with r.connect(host='localhost',port=28015,user='admin',db='rethinkdb').repl() as conn:
                db_table_user = r.db('rethinkdb').table('users').run()
                usrs_list = [user['id'] for user in db_table_user]
                if ('totalAmountBot_user' in usrs_list) == False:
                        r.db('rethinkdb').table('users').insert({'id':'totalAmountBot_user', 'password': 'totalAmountBot_user_pswd'}).run()
                else:
                        print('\n '+'totalAmount_user'+' user is already created\n')

                db_list = r.db_list().run()
                if ('totalAmountBot_db' in db_list) == False:
                        r.db_create('totalAmountBot_db').run()
                        r.db('totalAmountBot_db').table_create('totalAmountBot_table').run()
                        r.db('totalAmountBot_db').grant('totalAmountBot_user', {'read': True, 'write': True}).run()
                else:
                        print('\n '+'totalAmountBot_db'+' database is already created\n')

                print('DATABASES LIST:\n')
                db_list = r.db_list().run()
                print(db_list,'\n')

                print('USERS LIST:\n')
                db_table_user = r.db('rethinkdb').table('users').run()
                print(db_table_user,'\n')

                print('totalAmountBot_db TABLES LIST:\n')
                table_list_ = r.db('totalAmountBot_db').table_list().run()
                print(table_list_)

def getTablesFromBD():
        r = RethinkDB()
        with r.connect(host='localhost',port=28015,user='admin',db='rethinkdb').repl() as conn:
                totalTable = r.db('totalAmountBot_db').table('totalAmountBot_table').run()
                #print(len(list(totalTable)))
                for num, dict in enumerate(list(totalTable)):
                        print(f'---{num}---\n{dict}')

                #print(totalTable)

if __name__ == "__main__":
        #getTablesFromBD()
        createDB()




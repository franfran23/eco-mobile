import sqlite3

'''
def connect_db(host='localhost', user='root', password='', db=None):
	return mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=db)
'''
def connect_db(name='db.sqlite'):
	connection = sqlite3.connect(name)
	return connection, connection.cursor()


def list_users_except(username):
	db, cursor = connect_db()
	cursor.execute("SELECT username FROM identifiants")
	data = cursor.fetchall()
	users = []
	for user in data:
		if user[0] != username:
			users.append(user[0])
	return users
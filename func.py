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

jours = {1: 'Lundi',
			2: 'Mardi',
			3: 'Mercredi',
			4: 'Jeudi',
			5: 'Vendredi'}

def check_horaires(mes_horaires, autres_horaires):
	assert len(mes_horaires) == len(autres_horaires)
	# print(mes_horaires, autres_horaires) #
	correspondance = ''
	for i in range(len(mes_horaires)):
		assert mes_horaires[i][0] == autres_horaires[i][0]


		if mes_horaires[i][1] == '-':
			my_start, my_end = float('inf'), float('inf')
			# print('is -') #
		else:
			my_start, my_end = mes_horaires[i][1].split('-')
			my_start = int(my_start.split(':')[0]) * 60 + int(my_start.split(':')[1])
			my_end = int(my_end.split(':')[0]) * 60 + int(my_end.split(':')[1])
		# print(type(my_start)) #
		assert type(my_start) in [int, float]

		if autres_horaires[i][1] == '-':
			autre_start, autre_end = float('inf'), float('inf')
		else:
			autre_start, autre_end = autres_horaires[i][1].split('-')
			autre_start = int(autre_start.split(':')[0]) * 60 + int(autre_start.split(':')[1])
			autre_end = int(autre_end.split(':')[0]) * 60 + int(autre_end.split(':')[1])


		if abs(my_start - autre_start) <= 30:
			correspondance += jours[mes_horaires[i][0]] + ' matin, ' # écart de moins de 30 min le matin
		if abs(my_end - autre_end) <= 30:
			correspondance += jours[mes_horaires[i][0]] + ' soir, ' # écart de moins de 30 min le matin
	return correspondance
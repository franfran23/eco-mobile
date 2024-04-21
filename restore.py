import sqlite3
from cryptage import generate_fernet_key
from cryptography.fernet import Fernet

def connect_db(name='db.sqlite'):
	connection = sqlite3.connect(name)
	return connection, connection.cursor()

NEW_MASTER_KEY = ''
OLD_MASTER_KEY = ''

db, cursor = connect_db()

cursor.execute('SELECT id, sender, receiver, message FROM messages')
data = cursor.fetchall()

for each in data:
	id = int(each[0])
	sender = int(each[1])
	receiver = int(each[2])
	message = each[3].encode('utf-8')
	
	old_key = generate_fernet_key(OLD_MASTER_KEY, str(sender)+str(receiver))
	old_fernet = Fernet(old_key)
	
	message = old_fernet.decrypt(message) # message au format binaire
	
	new_key = generate_fernet_key(NEW_MASTER_KEY, str(sender)+str(receiver))
	new_fernet = Fernet(new_key)
	
	
	cursor.execute(f'UPDATE messages SET message = "{new_fernet.encrypt(message).decode("utf_8")}" WHERE id = {id} AND sender = {sender} AND receiver = {receiver};')

db.commit()

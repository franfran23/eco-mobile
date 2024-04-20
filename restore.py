# non testé

# import connect_db
from gen_keys import generate_fernet_key
from cryptography.fernet import Fernet

NEW_MASTER_KEY = ''
OLD_MASTER_KEY = ''

db, cursor = connect_db()

cursor.execute('SELECT id, user1, user2, message FROM messages')
data = cursor.fetchall()

for each in data:
	id = int(each[0])
	user1 = int(each[1])
	user2 = int(each[2])
	message = each[3]
	
	old_key = generate_fernet_key(OLD_MASTER_KEY, str(user1)+str(user2))
	old_fernet = Fernet(old_key)
	
	message = old_fernet.decrypt(message)
	
	new_key = generate_fernet_key(NEW_MASTER_KEY, str(user1)+str(user2))
	new_fernet = Fernet(new_key)
	
	
	cursor.execute(f'UPDATE messages SET message = "{new_fernet.encrypt(message)}" WHERE id = {id} AND user1 = "{user1}" AND user2 = "{user2}";')

db.commit()

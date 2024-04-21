from flask import Flask, url_for, request, redirect, render_template, make_response
from random import randint
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import mysql.connector
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from cryptography.fernet import Fernet, InvalidToken

from cryptage import generate_fernet_key, get_messages_fernet
MASTER_KEY = '_XB2fwMJpusNiZrnXZ8KLwHdL1_ld8G8XbAKJHZuMzk=' # Fernet.generate_key() # une nouvelle clé déconnectera toutes les sessions utilisateurs en cours

# pour encrypter les cookies (de session)
cookies_seed = 'cookies' # graine de génération de la clé de cryptage des cookies # on définira une vraie clé plus tard # une nouvelle clé déconnectera toutes les sessions utilisateurs en cours
cookies_key = generate_fernet_key(MASTER_KEY, cookies_seed) # clé de cryptage des cookies
# print('cookies key', cookies_key) #
cookies_fernet = Fernet(cookies_key)


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

def gen_db():
	tables = ['''CREATE TABLE identifiants (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nom VARCHAR(100),
	prenom VARCHAR(100),
	numero VARCHAR(10),
	username VARCHAR(255), -- Longueur maximale standard pour une adresse e-mail
	password VARCHAR(255), -- Longueur maximale pour le mot de passe
	creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	last_login TIMESTAMP,
	status BOOLEAN DEFAULT 0, -- TRUE pour activé, FALSE pour désactivé
	is_admin BOOLEAN DEFAULT 0 -- TRUE pour administrateur, FALSE pour utilisateur standard
);''',
'''CREATE TABLE messages (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	sender INTEGER,
	receiver INTEGER,
	message VARCHAR(2048), -- longueur maximum d'un message (crypté)
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	
	FOREIGN KEY(sender) REFERENCES identifiants(id),
	FOREIGN KEY(receiver) REFERENCES identifiants(id)
);''']
	for table in tables:
		try:
			cursor.execute(table)
		except:
			pass
	db.commit()

db, cursor = connect_db()

gen_db()


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
## socketio = SocketIO(app)
## CORS(app)


# FUNCTIONS

def check_credentials(username, password):
	# check les identifiants dans la db
	db, cursor = connect_db()
	try:
		cursor.execute(f'SELECT password, status FROM identifiants WHERE username = "{username}";')
		data = cursor.fetchone()
		hashed_pwd = data[0]
		status = bool(str(data[1])[0])
		if status:
			valid_auth = check_password_hash(hashed_pwd, password)
			if valid_auth:
				cursor.execute(f'UPDATE identifiants SET last_login = CURRENT_TIMESTAMP WHERE username = "{username}";')
				db.commit()
			return valid_auth
	except Exception as e:
		# print(e)
		pass
	return False

COOKIE_NAME = 'eco-mobile_login'
def get_username(request): # get username from crypted cookie
	try:
		cookie = request.cookies.get(COOKIE_NAME)
		if cookie is not None:
			username = cookies_fernet.decrypt(cookie.encode('utf-8')).decode('utf-8')
		else:
			username = None
	except InvalidToken:
		username = None
	return username

def send_email(username, code):
	# send an email with the random code inside
	# username is an e-mail address
	# (return if it works or not)
	print('code:', code)

def save_message(id_sender, id_receiver, message_clair):
	db, cursor = connect_db()
	fernet = get_messages_fernet(id_sender, id_receiver, MASTER_KEY) # objet fernet de cryptage entre id1 et id2
	message = fernet.encrypt(message_clair).decode('utf-8') # cryptage du message, stockage en utf-8
	cursor.execute(f'INSERT INTO messages (sender, receiver, message) VALUES ({id_sender}, {id_receiver}, "{message}");')
	db.commit()

def get_message(message_id):
	'''renvoie le message décrypté (prend l'id du message en paramètre)'''
	db, cursor = connect_db()
	cursor.execute(f'SELECT message, sender, receiver FROM messages WHERE id = {message_id};')
	data = cursor.fetchone()
	if data is None:
		return 'Wrong id'
	crypted_message = data[0].encode('utf-8')
	id_sender = data[1]
	id_receiver = data[2]
	
	fernet = get_messages_fernet(id_sender, id_receiver, MASTER_KEY)
	try:
		return fernet.decrypt(crypted_message).decode('utf-8')
	except InvalidToken:
		return ''




# FLASK SERVER
@app.route('/')
def index():
	message = request.args.get('message') or ''
	
	username = get_username(request)
	
	if username is None:
		username = 'Not Connected'
	else:
		username = 'Connected as ' + str(username)
	return render_template('index.html', message=message, connexion=username)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		db, cursor = connect_db()
		nom = request.form['nom']
		prenom = request.form['prenom']
		username = request.form['email']
		numero = request.form['numero'][:10]
		password = generate_password_hash(request.form['password'])
		
		cursor.execute(f'SELECT COUNT(*) FROM identifiants WHERE username = "{username}";')
		if int(cursor.fetchone()[0]) > 0:
			return redirect('/?message=Un utilisateur a déjà été créé avec cette addresse mail. Veuillez ressayer.')
		
		code = str(randint(1000, 9999))
		send_email(username, code)
		cursor.execute(f'INSERT INTO identifiants (nom, prenom, numero, username, password, status) VALUES ("{nom}","{prenom}","{numero}","{username}","{password}", "{"0"+generate_password_hash(code)}");')
		db.commit()
		return redirect(f'/verif?username={username}')
	
	return render_template('inscription.html')

@app.route('/verif', methods=['GET', 'POST'])
def verif():
	if request.method == 'POST':
		username = request.form['username']
		code = request.form['code']
		db, cursor = connect_db()
		cursor.execute(f'SELECT status from identifiants WHERE username = "{username}";')
		status = cursor.fetchone()[0]
		if status[0] == '0':
			hashed_code = status[1:]
			if check_password_hash(hashed_code, code):
				cursor.execute(f'UPDATE identifiants SET status = 1 WHERE username = "{username}";')
				db.commit()
				return redirect('/?message=Votre compte à bien été activé, vous pouvez vous connecter')
			return redirect('/?message=Le code que vous avez entré est incorrecte, veuillez réessayer.')
		else:
			return redirect('/?message=Erreur à l\'inscription, veuillez contacter un administrateur.')
	
	return render_template('verif.html', username=request.args.get('username'))



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if check_credentials(username, password):
			response = make_response(redirect('/?message=Login Successful'))
			response.set_cookie(COOKIE_NAME, cookies_fernet.encrypt(username.encode('utf-8')).decode('utf-8'), secure=True, httponly=True)
			return response
		return redirect('/?message=Invalid username or password (Maybe your account is disabled. If the issue persist, please contact an administrator)')

	return render_template('login.html')

@app.route('/logout')
def logout():
	response = make_response(redirect('/?message=Logout Successful'))
	response.delete_cookie(COOKIE_NAME)
	return response


# developpement test
'''
@app.route('/save')
def save_msg():
	message = request.args.get('msg')
	save_message(1, 2, message.encode('utf-8'))
	return 'done'
@app.route('/see')
def see():
	id = int(request.args.get('id'))
	return get_message(id)
'''


# SOCKETIO SERVER
'''
@socketio.on('connect')
def handle_connect():
	print('Connected')

@socketio.on('disconnect')
def handle_disconnect():
	print('Disconnected')

@socketio.on('message')
def handle_message(message):
	print('Received message:', message)
	emit('message', message, broadcast=True)
'''

if __name__ == '__main__':
	app.run(debug=True)
	# socketio.run(app, debug=True, use_reloader=True, allow_unsafe_werkzeug=True)
	

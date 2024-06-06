from flask import Flask, url_for, request, redirect, render_template, make_response, session
from random import randint
from flask_socketio import SocketIO, emit, join_room
# from flask_cors import CORS
# import mysql.connector
from os.path import exists
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from cryptography.fernet import Fernet, InvalidToken


from cryptage import *
MASTER_KEY = '_XB2fwMJpusNiZrnXZ8KLwHdL1_ld8G8XbAKJHZuMzk=' # Fernet.generate_key() # une nouvelle clé déconnectera toutes les sessions utilisateurs en cours

cookies_fernet = get_cookies_fernet(MASTER_KEY)


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
	lat REAL,
	long REAL,
	username VARCHAR(255), -- Longueur maximale standard pour une adresse e-mail
	password VARCHAR(255), -- Longueur maximale pour le mot de passe
	creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	last_login TIMESTAMP,
	status BOOLEAN DEFAULT 0, -- TRUE pour activé, FALSE pour désactivé
	is_admin BOOLEAN DEFAULT 0 -- TRUE pour administrateur, FALSE pour utilisateur standard
);''',
'''CREATE TABLE horaires (
	user_id INT, 
	jour INT NOT NULL, 
	horaire VARCHAR(11), 

	PRIMARY KEY(user_id, jour),
	FOREIGN KEY(user_id) REFERENCES identifiants(id)
);''']
	for table in tables:
		try:
			cursor.execute(table)
		except Exception as e:
			pass
	db.commit()


db, cursor = connect_db()
gen_db()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")
## CORS(app)

@app.before_request
def before_request():
	print('path is', request.path)
	print(get_username(request))
	if not get_username(request) and not (request.path.endswith('.css') or request.path.endswith('.js') or request.path.endswith('.png') or request.path.endswith('.jpg') or request.path.endswith('.ico') or request.path.startswith('/login') or request.path.startswith('/signup') or request.path.startswith('/verif')):
		return redirect('/login?message=Veuillez vous connecter pour continuer')

# FUNCTIONS

def check_credentials(username, password):
	# check les identifiants dans la db
	db, cursor = connect_db()
	try:
		cursor.execute(f"SELECT password, status FROM identifiants WHERE username = '{username}';")
		data = cursor.fetchone()
		hashed_pwd = data[0]
		status = bool(int(str(data[1])[0]))
		if status:
			valid_auth = check_password_hash(hashed_pwd, password)
			if valid_auth:
				cursor.execute(f"UPDATE identifiants SET last_login = CURRENT_TIMESTAMP WHERE username = '{username}';")
				db.commit()
			return valid_auth
	except Exception as e:
		print(e)
		pass
	return False


def get_username(request): # get username from crypted cookie
	try:
		cookie = request.cookies.get(COOKIE_NAME)
		if cookie is not None:
			username = get_cookies_fernet(MASTER_KEY).decrypt(cookie.encode('utf-8')).decode('utf-8')
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
	cursor.execute(f"INSERT INTO messages (sender, receiver, message) VALUES ({id_sender}, {id_receiver}, '{message}');")
	db.commit()

def get_message(message_id):
	'''renvoie le message décrypté (prend l'id du message en paramètre)'''
	db, cursor = connect_db()
	cursor.execute(f"SELECT message, sender, receiver FROM messages WHERE id = {message_id};")
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
		username = 'Déconnecté(e)'
	else:
		username = 'Connecté(e) en tant que ' + str(username)
	
	return render_template('index.html', message=message, connexion=username)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		try:
			db, cursor = connect_db()
			# print('form', request.form)
			nom = request.form['nom']
			prenom = request.form['prenom']
			username = request.form['email']
			numero = request.form['numero'][:10]
			lat = request.form['lat']
			long = request.form['long']
			# horaires gérés plus tard
			password = generate_password_hash(request.form['password'])
			
			cursor.execute(f"SELECT COUNT(*) FROM identifiants WHERE username = '{username}';")
			if int(cursor.fetchone()[0]) > 0:
				return redirect('/?message=Un utilisateur a déjà été créé avec cette adresse mail. Veuillez réessayer.')

			code = str(randint(1000, 9999))
			send_email(username, code)
			
			cursor.execute(f"INSERT INTO identifiants (nom, prenom, numero, lat, long, username, password, status) VALUES ('{nom}','{prenom}','{numero}',{lat},{long},'{username}','{password}', '{'0'+generate_password_hash(code)}');")
			db.commit()
			cursor.execute(f"SELECT id FROM identifiants WHERE username = '{username}';")
			user_id = cursor.fetchone()[0]
			if user_id is None:
				return redirect("/?message=Erreur dans l'enregistrement de votre compte, veuillez contacter un administrateur.")
			
			jours = {'Lundi': 1,
			'Mardi': 2,
			'Mercredi': 3,
			'Jeudi': 4,
			'Vendredi': 5}

			for jour in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']:
				cursor.execute(f"INSERT INTO horaires (user_id, jour, horaire) VALUES ({user_id}, {jours[jour]}, '{request.form['start' + jour] + '-' + request.form['end' + jour]}');")
			db.commit()

			return redirect(f'/verif?username={username}')
		except Exception as e:
			print('Erreur dans le traitement de l\'inscription de', username, ': ', e)
			return redirect('/?message=Une erreur est survenue.')
	
	return render_template('inscription.html')

@app.route('/verif', methods=['GET', 'POST'])
def verif():
	if request.method == 'POST':
		username = request.form['username']
		code = request.form['code']
		db, cursor = connect_db()
		cursor.execute(f"SELECT status from identifiants WHERE username = '{username}';")
		status = cursor.fetchone()[0]
		if status[0] == '0':
			hashed_code = status[1:]
			if check_password_hash(hashed_code, code):
				cursor.execute(f"UPDATE identifiants SET status = 1 WHERE username = '{username}';")
				db.commit()
				return redirect('/?message=Votre compte a bien été activé, vous pouvez vous connecter')
			return redirect('/verif?message=Le code que vous avez entré est incorrect. Veuillez réessayer.')
		else:
			return redirect('/?message=Erreur à l\'inscription. Veuillez contacter un administrateur.')
	
	return render_template('verif.html', username=request.args.get('username'), message=(request.args.get('message') or ''))



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if check_credentials(username, password):
			response = store_session_cookie(username, MASTER_KEY)
			return response
		return redirect('/?message=Identifiant et/ou mot de passe invalide(s). Il se peut que votre compte soit désactivé. Dans ce cas, merci de contacter un administrateur.')

	return render_template('login.html')

@app.route('/logout')
def logout():
	response = make_response(redirect('/?message=Déconnecté(e)'))
	remove_cookie(response)
	return response



@app.route('/contacts')
def contacts():
	db, cursor = connect_db()
	cursor.execute(f"SELECT nom, prenom, username FROM identifiants WHERE username != '{get_username(request)}' ORDER BY last_login;")
	contacts = cursor.fetchall()
	return render_template('contacts.html', contacts=contacts)

@app.route('/chat')
def chat():
	sender = get_username(request)
	if sender is None:
		return redirect('/?message=Vous n\'êtes pas connecté(e).')
	receiver = request.args.get('contact') or None
	if receiver is None:
		receiver = 'username'
		# sélection du contact le plus récent
	session['receiver'] = receiver
	session['me'] = sender
	return render_template('chat.html', name=receiver)


@app.route('/account')
def account():
	return render_template('account.html')


@app.route('/gps', methods=['GET', 'POST'])
def gps():
	if request.method == 'POST':
		lat = request.form['lat']
		long = request.form['long']
		return f'latitude: {lat}, longitude: {long}'
	return render_template('openstreetmap_test.html')


# SOCKETIO SERVER

@socketio.on('connect')
def handle_connect():
	# print(session['me'], 'connected to', session['receiver'])
	join_room(session['me'])


@socketio.on('disconnect')
def handle_disconnect():
	# print(session['me'], 'disconnected', session['receiver'])
	pass

@socketio.on('message')
def handle_message(message: str):
	# print('Received message :', message, 'from', session['me'], 'to', session['receiver'])
	emit('message', message, room=session['receiver'])

	# save message
	db, cursor = connect_db()
	def get_user_id(username):
		cursor.execute(f"SELECT id FROM identifiants WHERE username = '{username}';")
		data = cursor.fetchone()
		if data is None:
			print('Error while saving message:')
			print('From', session['me'], 'to', session['receiver'])
			print('message:', message)
			return None
		return int(data[0])
	sender_id = get_user_id(session['me'])
	receiver_id = get_user_id(session['receiver'])
	if sender_id is None or receiver_id is None:
		return 'message not saved, error occured'
	
	fernet = get_cookies_fernet(sender_id, receiver_id, MASTER_KEY)
	cursor.execute(f"INSERT INTO messages (message, sender, receiver) VALUES ('{fernet.encrypt(message.encode('utf-8')).decode('utf-8')}', {sender_id}, {receiver_id});")
	db.commit()

if __name__ == '__main__':
	# app.run(debug=True)
	socketio.run(app, debug=True)
	

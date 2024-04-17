from flask import Flask, url_for, request, redirect, render_template, make_response
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import mysql.connector
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from cryptography.fernet import Fernet, InvalidToken
cle = '_XB2fwMJpusNiZrnXZ8KLwHdL1_ld8G8XbAKJHZuMzk=' # Fernet.generate_key()
fernet = Fernet(cle)

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
    status BOOLEAN DEFAULT 1, -- TRUE pour activé, FALSE pour désactivé
    is_admin BOOLEAN DEFAULT 0 -- TRUE pour administrateur, FALSE pour utilisateur standard
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

def check_credentials(username, password):
	# check, les identifiants dans la db
	db, cursor = connect_db()
	try:
		cursor.execute(f'SELECT password, status FROM identifiants WHERE username = "{username}";')
		data = cursor.fetchone()
		hashed_pwd = data[0]
		status = bool(data[1])
		print('status', status)
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

# FLASK SERVER
@app.route('/')
def index():
	message = request.args.get('message') or ''
	
	try:
		cookie = request.cookies.get('username')
		if cookie is not None:
			username = fernet.decrypt(cookie.encode('utf-8')).decode('utf-8')
		else:
			username = ''
	except InvalidToken:
		username = ''
	
	if username == '':
		username = 'Not Connected'
	else:
		username = 'Connected as ' + str(username)
	return render_template('index.html', message=message, connexion=username)


@app.route('/signup', methods=['GET', 'POST'])
def signin():
	db, cursor = connect_db()
	if request.method == 'POST':
		nom = request.form['nom']
		prenom = request.form['prenom']
		username = request.form['email']
		numero = request.form['numero'][:10]
		password = generate_password_hash(request.form['password'])
		
		cursor.execute(f'SELECT COUNT(*) FROM identifiants WHERE username = "{username}";')
		if int(cursor.fetchone()[0]) > 0:
			return redirect('/?message=Un utilisateur a déjà été créé avec cette addresse mail. Veuillez ressayer.')
		
		cursor.execute(f'INSERT INTO identifiants (nom, prenom, numero, username, password) VALUES ("{nom}","{prenom}","{numero}","{username}","{password}");')
		db.commit()
		return redirect('/?message=Signed In Successfully')
	
	return render_template('inscription.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if check_credentials(username, password):
			response = make_response(redirect('/?message=Login Successful'))
			response.set_cookie('username', fernet.encrypt(username.encode('utf-8')).decode('utf-8'), secure=True, httponly=True)
			return response
		return redirect('/?message=Invalid username or password (Maybe your account is disabled. If the issue persist, please contact an administrator)')

	return render_template('login.html')

@app.route('/logout')
def logout():
	response = make_response(redirect('/?message=Logout Successful'))
	response.delete_cookie('username')
	return response

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
	

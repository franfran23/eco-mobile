from flask import Flask, url_for, request, redirect, render_template, make_response
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import mysql.connector
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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
	return connection

def gen_db():
	tables = ['CREATE TABLE test']
	for table in tables:
		try:
			cursor.execute(table)
		except:
			pass
	db.commit()

db = connect_db()
cursor = db.cursor()

gen_db()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
## socketio = SocketIO(app)
## CORS(app)

def check_credentials(username, password):
	# check, les identifiants dans la db
	return True # test
	return check_password_hash(hashed_pwd, password)

# FLASK SERVER
@app.route('/')
def index():
	message = request.args.get('message') or ''
	username = request.cookies.get('username') or ''
	if username == '':
		username = 'Not Connected'
	else:
		username = 'Connected as ' + str(username)
	return render_template('index.html', message=message, connexion=username)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		nom = request.form['nom']
		prenom = request.form['prenom']
		username = request.form['email']
		numero = request.form['numero']
		password = generate_password_hash(request.form['password'])

		# requète sql
	return render_template('inscription.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		data = request.form
		username = data.get('username')
		password = data.get('password')
		if check_credentials(username, password):
			response = make_response(render_template('index.html', message='Login Successful'))
			response.set_cookie('username', username)
			return response
		return render_template('index.html', message='Invalid username or password')

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
	

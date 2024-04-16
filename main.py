from flask import Flask, url_for, request, redirect, render_template, make_response
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import mysql.connector

from datetime import timedelta

'''
def connect_db(host='localhost', user='root', password='', db=None):
	return mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=db)

db = connect_db(user='testuser', password='testuser', db='eco-mobile')
cursor = db.cursor()'''

app = Flask(__name__)
app.secret_key = 'SECRET KEY'
## socketio = SocketIO(app)
## CORS(app)

def check_credentials(username, password):
	# check, les identifiants dans la db
	return True # test
	return username=='username' and password=='pwd'

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
	

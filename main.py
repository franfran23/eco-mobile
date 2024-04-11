from flask import Flask, url_for, request, redirect, render_template, session
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
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
## socketio = SocketIO(app)
## CORS(app)

def check_credentials(username, password):
	# check, les identifiants dans la db
	return username=='username' and password=='pwd'

# FLASK SERVER
@app.route('/')
def index():
	message = request.args.get('message') or ''
	return render_template('index.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if check_credentials(request.form['username'], request.form['password']):
			session['logged_in'] = True
			return redirect(url_for('index'), message="Logged in")

	return render_template('login.html')

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
	

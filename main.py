from flask import Flask, url_for, request, redirect, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
# import mysql.connector

'''
def connect_db(host='localhost', user='root', password='', db=None):
	return mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=db)

db = connect_db(user='testuser', password='testuser', db='suivi_medical')
cursor = db.cursor()'''

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

# FLASK SERVER
@app.route('/')
def index():
	return render_template('index.html')

# SOCKETIO SERVER
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


if __name__ == '__main__':
	socketio.run(app, debug=True, use_reloader=True, allow_unsafe_werkzeug=True)
	

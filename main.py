from flask import Flask, url_for, request, redirect
import mysql.connector

def connect_db(host='localhost', user='root', password='', db=None):
	return mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=db)

db = connect_db(user='testuser', password='testuser', db='suivi_medical')
cursor = db.cursor()

app = Flask(__name__)


@app.route('/')
def index():
	return open('index.html', 'r', encoding='utf8').read()
# we need to add some more dependencies
# flask-sqlalchemy for the database
# flask-cas for CAS authentication
# 

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_mail import Mail

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = 'sqlite:///' + os.path.join(basedir, 'tigertask.sqlite')

app.config.update(

	# DB SETTINGS
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	SQLALCHEMY_DATABASE_URI = database_uri,

	# EMAIL SETTINGS
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	
	)

db = SQLAlchemy(app)
admin = Admin(app)
mail = Mail(app)

# Generated by os.urandom(16)
app.secret_key = b'\xcdt\x8dn\xe1\xbdW\x9d[}yJ\xfc\xa3~/'

is_heroku = os.environ.get("IS_HEROKU", None)

if is_heroku:
   print("We are in Heroku")
   app.config["DEBUG"] = False
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']



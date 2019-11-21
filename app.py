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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tigertask.sqlite')
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



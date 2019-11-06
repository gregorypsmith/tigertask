# we need ot add some more dependencies
# flask-sqlalchemy for the database
# flask-cas for CAS authentication
# 

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from utils import is_heroku

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "thisisasecret"
if is_heroku():
    app.config["DEBUG"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tigertask.sqlite')

db = SQLAlchemy(app)
admin = Admin(app)



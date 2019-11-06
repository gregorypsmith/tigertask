import os

from app import db, admin, mail
from flask_admin.contrib.sqla import ModelView


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

admin.add_view(ModelView(User, db.session))

db.create_all()



    
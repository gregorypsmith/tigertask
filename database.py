import os

from app import db, admin, mail
from flask_admin.contrib.sqla import ModelView


class Customer(db.Model):
	custid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode)
	email = db.Column(db.Unicode)
	password = db.Column(db.Unicode)

class Deliverer(db.Model):
	delivid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode)
	phone_number = db.Column(db.Unicode)
	email = db.Column(db.Unicode)
	password = db.Column(db.Unicode)

class Cart(db.Model):
	custid = db.Column(db.Integer, primary_key=True)
	itemid = db.Column(db.Integer)
	quantity = db.Column(db.Integer)

class Order(db.Model):
	orderid = db.Column(db.Integer, primary_key=True)
	custid = db.Column(db.Integer)
	delivid = db.Column(db.Integer)

class OrderItem(db.Model):
	orderid = db.Column(db.Integer, primary_key=True)
	itemid = db.Column(db.Integer)
	quantity = db.Column(db.Integer)

class Inventory(db.Model):
	itemid = db.Column(db.Integer, primary_key=True)
	item_name = db.Column(db.Unicode)
	price = db.Column(db.Integer)
	category = db.Column(db.Unicode)


admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Deliverer, db.session))
admin.add_view(ModelView(Cart, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderItem, db.session))
admin.add_view(ModelView(Inventory, db.session))

db.create_all()



    
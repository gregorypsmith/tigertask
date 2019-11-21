import os

from app import db, admin, mail
from flask_admin.contrib.sqla import ModelView


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode)
	phone_number = db.Column(db.Unicode)
	email = db.Column(db.Unicode)
	orders = db.relationship('Order', backref='Customer')
	cartitems = db.relationship('CartItem', backref='Customer')

class Deliverer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode)
	phone_number = db.Column(db.Unicode)
	email = db.Column(db.Unicode)

	orders = db.relationship('Order', backref='Deliverer')

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode)
	price = db.Column(db.Integer)
	category = db.Column(db.Unicode)

	orderitems = db.relationship('OrderItem', backref='Item')
	cartitems = db.relationship('CartItem', backref='Item')

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	custid = db.Column(db.Integer, db.ForeignKey(Customer.id))
	delivid = db.Column(db.Integer, db.ForeignKey(Deliverer.id))
	status = db.Column(db.Unicode)
	building = db.Column(db.Unicode)
	roomnum = db.Column(db.Unicode)
	note = db.Column(db.Unicode)

	orderitems = db.relationship('OrderItem', backref='Order')

class CartItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	custid = db.Column(db.Integer, db.ForeignKey(Customer.id))
	itemid = db.Column(db.Integer, db.ForeignKey(Item.id))
	quantity = db.Column(db.Integer)

class OrderItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	orderid = db.Column(db.Integer, db.ForeignKey(Order.id))
	itemid = db.Column(db.Integer, db.ForeignKey(Item.id))
	quantity = db.Column(db.Integer)


admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Deliverer, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(CartItem, db.session))
admin.add_view(ModelView(OrderItem, db.session))

if __name__ == '__main__':
	db.create_all()



    
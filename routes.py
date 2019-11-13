from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

@app.route("/homecustomer")
def homecustomer():
    return render_template('homecustomer.html')

@app.route("/homedeliver")
def homedeliver():
    return render_template('homedeliver.html')

@app.route("/deliveries")
def deliveries():
    return render_template('deliveries.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/about")
def about():
    return render_template('about.html')
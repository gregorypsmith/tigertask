from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')
from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template, request, make_response
from CASClient import  CASClient

@app.route("/")
@app.route("/index")
def home():

    username = CASClient().authenticate()
    return render_template('index.html')

@app.route("/homecustomer")
def homecustomer():

    username = CASClient().authenticate()

    query = request.args.get('query')

    if query is None:
    	query = ""

    items = Item.query.filter(Item.name.contains(query))

    results = []
    for item in items:
        results.append({
            "name": item.name,
            "price": item.price,
            "category": item.category,
        })
    html = render_template('homecustomer.html', 
    items=results, 
    prevQuery=query)
    response = make_response(html)

    return response

@app.route("/homedeliver")
def homedeliver():
    username = CASClient().authenticate()
    return render_template('homedeliver.html')

@app.route("/deliveries")
def deliveries():
    username = CASClient().authenticate()
    return render_template('deliveries.html')

@app.route("/cart")
def cart():
    username = CASClient().authenticate()
    return render_template('cart.html')


@app.route("/about")
def about():
    username = CASClient().authenticate()
    return render_template('about.html')
from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template, request, make_response
from CASClient import CASClient

@app.route("/")
@app.route("/index")
def home():

    username = CASClient().authenticate()

    user = Customer.query.filter_by(email=str(username + "@princeton.edu")).first()

    if user is None:
        return createaccount()
    
    return render_template('index.html')

@app.route('/createaccount')
def createaccount():

    username=CASClient().authenticate()

    fname = request.args.get('firstname')
    lname = request.args.get('lastname')
    phone = request.args.get('phone')

    if fname is None or lname is None or phone is None:
        return render_template('createaccount.html', errorMsg="Please enter your information below.")

    newcust = Customer(name=str(fname + ' ' + lname), phone_number=phone, email=str(username + "@princeton.edu"))
    newdeliv = Deliverer(name=str(fname + ' ' + lname), phone_number=phone, email=str(username.strip() + "@princeton.edu"))
    
    #newcust = Customer()
    #newcust.name.append(str(fname + ' ' + lname))
    #newcust.phone_number.append(phone)
    #newcust.email.append(str(username + "@princeton.edu"))
    db.session.add(newcust)
    db.session.add(newdeliv)
    db.session.commit()

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
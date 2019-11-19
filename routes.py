from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template, request, make_response
from CASClient import CASClient

@app.route("/")
@app.route("/index")
def home():

    username = CASClient().authenticate()

    user = Customer.query.filter_by(email=str(username.strip() + "@princeton.edu")).first()

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

    newcust = Customer(name=str(fname + ' ' + lname), phone_number=phone, email=str(username.strip() + "@princeton.edu"))
    newdeliv = Deliverer(name=str(fname + ' ' + lname), phone_number=phone, email=str(username.strip() + "@princeton.edu"))
    
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
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "category": item.category,
        })
    html = render_template('homecustomer.html', 
    items=results, 
    prevQuery=query
    )

    # add one of this item to the cartitems page
    itemid = request.args.get('added')
    cust = Customer.query.filter_by(email=str(username.strip() + "@princeton.edu")).first()

    item = CartItem.query.filter_by(Customer=cust, itemid=itemid).first()

    if item is None:
        newitem = CartItem(custid=cust.id, itemid=itemid, quantity=int(1))
        db.session.add(newitem)
        db.session.commit()
    
    else:
        item.quantity = item.quantity + 1
        db.session.commit()


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
    email = username + "@princeton.edu"
    cust = Customer.query.filter_by(email=email).first()
    cart_items = CartItem.query.filter_by(Customer=cust).all()
    names = []
    prices = []
    quantities = []
    total = 0
    for item in cart_items:
        names.append(item.name)
        prices.append(item.price)
        quantities.append(item.quantity)
        total += item.Item.price * item.quantity
        

    return render_template('cart.html', cart=(names, prices, quantities), total_price=total)


@app.route("/about")
def about():
    username = CASClient().authenticate()
    return render_template('about.html')

@app.route("/placeorder")
def placeorder():
    username = CASClient().authenticate()
    email = username + "@princeton.edu"
    cust = Customer.query.filter_by(email=email).first()
    cart_items = CartItem.query.filter_by(Customer=cust).all()

    for item in cart_items:
        newitem = OrderItem(quantity=item.quantity, Item=item, Customer=cust)
        db.session.add(newitem)
        db.session.delete(item)
        db.session.commit()
        

@app.route("/orders")
def orders():
    username = CASClient().authenticate()
    return render_template('orders.html')
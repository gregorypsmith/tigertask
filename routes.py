from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template, request, make_response
from CASClient import CASClient
from datetime import datetime
import stripe
import urllib

BEING_DELIVERED = "Being Delivered"
DELIVERED = "Delivered"
WAITING = "Waiting for Deliverer"

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
    category = request.args.get('category')

    if query is None:
    	query = ""

    items = Item.query.filter(Item.name.contains(query)).all()

    if category is not None:
        if category != 'All':
            items = Item.query.filter(Item.name.contains(query)).filter_by(category=category).all()
    else:
        category = "All"
    results = []
    for item in items:
        results.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "category": item.category,
        })

    # add this item to the cartitems page
    itemid = request.args.get('added')
    quant = request.args.get('quantity')
    if itemid is None:
        html = render_template('homecustomer.html', 
        items=results, 
        prevQuery=query,
        addedMsg='',
        category=category,
        )
        response = make_response(html)
        return response
        
    cust = Customer.query.filter_by(email=str(username.strip() + "@princeton.edu")).first()

    item = CartItem.query.filter_by(Customer=cust, itemid=itemid).first()

    if item is None:
        newitem = CartItem(custid=cust.id, itemid=itemid, quantity=quant)
        db.session.add(newitem)
        db.session.commit()
    
    else:
        item.quantity = item.quantity + int(quant)
        db.session.commit()
    
    addedMsg=''
    
    if request.args.get('added'):
        added = CartItem.query.filter_by(itemid=request.args.get('added')).first()
        addeditem = Item.query.filter_by(id=added.itemid).first()
        addedMsg = str(addeditem.name + ' successfully added to cart!')

    html = render_template('homecustomer.html', 
    items=results, 
    prevQuery=query,
    addedMsg=addedMsg,
    category=category,
    )

    response = make_response(html)

    return response

@app.route("/homedeliver")
def homedeliver():
    username = CASClient().authenticate()
    deliv = Deliverer.query.filter_by(email=str(username.strip() + "@princeton.edu")).first()

    orders = Order.query.filter_by(status="Waiting for Deliverer").all()

    results = []
    for order in orders:
        cust = Customer.query.filter_by(id=order.custid).first()
        results.append({
            "id": order.id,
            "name": cust.name,
            "phone_number": cust.phone_number,
            "building": order.building,
            "roomnum": order.roomnum,
            "price": order.price,
            "time_placed": order.time_placed,
        })

    return render_template('homedeliver.html', results=results)

@app.route("/deliveries")
def deliveries():
    username = CASClient().authenticate()
    deliv = Deliverer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()
    orders = Order.query.filter_by(Deliverer=deliv).all()

    results = []
    for order in orders:
        cust = Customer.query.filter_by(id=order.custid).first()
        results.append({
            "id": order.id,
            "name": order.Customer.name,
            "phone_number": cust.phone_number,
            "building": order.building,
            "roomnum": order.roomnum,
            "price": order.price,
            "time_placed": order.time_placed,
            "status": order.status,
        })

    return render_template('deliveries.html', results=results)

@app.route("/cart")
def cart():

    username = CASClient().authenticate()

    email = username.strip() + "@princeton.edu"
    cust = Customer.query.filter_by(email=email).first()

    removed_id = request.args.get('removed_id')
    if removed_id is not None:
        removed_cart_item = CartItem.query.filter_by(Customer=cust, itemid=removed_id).first()
        if removed_cart_item:
            db.session.delete(removed_cart_item)
            db.session.commit()

    cart_items = CartItem.query.filter_by(Customer=cust).all()

    results = []
    subtotal = 0
    fee = 0
    for cart_item in cart_items:
        item = Item.query.filter_by(id=cart_item.itemid).first()
        
        if item is not None:
            results.append({
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "category": item.category,
                "quantity": cart_item.quantity
            })
            subtotal += item.price * cart_item.quantity

        if subtotal > 0:
            fee = 1.99
        if subtotal > 10:
            fee = 2.99
        if subtotal > 25:
            fee = 3.99
    
    total = '%.2f'%(subtotal + fee)
    subtotal = '%.2f'%(subtotal)

    buildfile = open(r"buildings.txt", "r")
    buildings = []
    building = buildfile.readline()
    while building is not '':
        buildings.append(building)
        building = buildfile.readline()
    buildfile.close()

    return render_template('cart.html', cart=results, subtotal=subtotal, fee=fee, total=total, buildings=buildings)

@app.route("/about")
def about():
    username = CASClient().authenticate()
    return render_template('about.html')

@app.route("/pay")
def pay():

    username = CASClient().authenticate()
    stripe.api_key = 'sk_live_s7cVmV1jM2a5IKAKFv1PISOl00CkFtmnW4'

    total = request.args.get('total')
    building = request.args.get('building')
    roomnum = request.args.get('roomnum')
    note = request.args.get('note')

    session = stripe.checkout.Session.create(
    customer_email=str(username.strip() + '@princeton.edu'),
    payment_method_types=['card'],
    line_items=[{
        'name': 'Confirm Order',
        'description': 'We will get these items to you in a jif!',
        'images': ['https://www.cs.princeton.edu/sites/all/modules/custom/cs_people/generate_thumbnail.php?id=12&thumb='],
        'amount': 50,
        'currency': 'usd',
        'quantity': 1,
    }],
    success_url=str('https://tigertask.herokuapp.com/placeorder?building=' + urllib.parse.quote(building) + \
         '&roomnum=' + urllib.parse.quote(roomnum) + '&note=' + urllib.parse.quote(note)),
    cancel_url='https://tigertask.herokuapp.com/cart',
    )
    return render_template('placingorder.html', sessionid=session.id)

@app.route("/placeorder")
def placeorder():

    username = CASClient().authenticate()
    cust = Customer.query.filter_by(email=str(username.strip() + "@princeton.edu")).first()
    cart_items = CartItem.query.filter_by(Customer=cust).all()

    subtotal = 0
    fee = 0
    for cart_item in cart_items:
        item = Item.query.filter_by(id=cart_item.itemid).first()
        if item is not None:
            subtotal += item.price * cart_item.quantity

        if subtotal > 0:
            fee = 1.99
        if subtotal > 10:
            fee = 2.99
        if subtotal > 25:
            fee = 3.99
    
    total = '%.2f'%(subtotal + fee)
    building = request.args.get('building')
    roomnum = request.args.get('roomnum')
    note = request.args.get('note')

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # prevents adding order multiple times when refreshing
    if fee > 0:
        order = Order(Customer=cust, status="Waiting for Deliverer", building=building, roomnum=roomnum, note=note, price=total, time_placed=dt_string)
        db.session.add(order)
        db.session.commit()

    for item in cart_items:
        newitem = OrderItem(quantity=item.quantity, itemid=item.itemid, Order=order)
        db.session.add(newitem)
        db.session.delete(item)
        db.session.commit()

    delivered = request.args.get('delivered')
    if delivered:
        print(delivered)
        if delivered == 'True':
            deliv_id = request.args.get('delivered_id')
            print(deliv_id)
            delivered = Order.query.filter_by(id=deliv_id).first()
            delivered.status = 'Delivered'
            db.session.commit()

    canceled = request.args.get('canceled')
    if canceled is not None:
        removed_order = Order.query.filter_by(id=canceled).first()
        if removed_order is not None:
            print("removing order")
            db.session.delete(removed_order)
            db.session.commit()

    orders = Order.query.filter_by(Customer=cust).all()
    result = []
    for order in orders:
        
        if order.Deliverer is None:
            deliverer = "None"
        else:
            deliverer = order.Deliverer.name
        result.append({
            "id": order.id,
            "customer": order.Customer.name,
            "deliverer": deliverer,
            "status": order.status,
        })
    return render_template('orders.html', orders=result, status="All")

@app.route("/claimorder")
def claimorder():
    username = CASClient().authenticate()
    deliv = Deliverer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()

    id = request.args.get('claimed_id')
    order = Order.query.filter_by(id=id).first()

    if order is not None:
        order.status = "Being Delivered"
        order.Deliverer = deliv
        db.session.commit()


    orders = Order.query.filter_by(status="Waiting for Deliverer").all()

    results = []
    for order in orders:
        cust = Customer.query.filter_by(id=order.custid).first()
        results.append({
            "id": order.id,
            "name": order.Customer.name,
            "phone_number": cust.phone_number,
            "building": order.building,
            "roomnum": order.roomnum,
            "price": order.price,
            "time_placed": order.time_placed,
            "status": order.status,
        })

    return render_template('deliveries.html', results=results)

@app.route("/orders")
def orders():
    username = CASClient().authenticate()
    
    customer = Customer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()
    
    delivered = request.args.get('delivered')
    if delivered:
        print(delivered)
        if delivered == 'True':
            deliv_id = request.args.get('delivered_id')
            print(deliv_id)
            delivered = Order.query.filter_by(id=deliv_id).first()
            delivered.status = 'Delivered'
            db.session.commit()

    canceled = request.args.get('canceled')
    if canceled is not None:
        removed_order = Order.query.filter_by(id=canceled).first()
        if removed_order is not None:
            print("removing order")
            db.session.delete(removed_order)
            db.session.commit()

    status = request.args.get('status')
    if status is None or status == 'All':
        status = "All"
        orders = Order.query.filter_by(Customer=customer).all()
    else:
        orders = Order.query.filter_by(Customer=customer, status=status).all()

    result = []
    print(orders)
    for order in orders:
        deliverer_name = 'None'
        deliverer_num = 'None'
        if order.Deliverer:
            deliverer_name = order.Deliverer.name
            deliverer_num = order.Deliverer.phone_number
        result.append({
            "id": order.id,
            "customer": order.Customer.name,
            "deliverer": deliverer_name,
            "deliverer_num": deliverer_num,
            "status": order.status,
        })

    return render_template('orders.html', orders=result, status=status)


@app.route("/orderdetails")
def orderdetails():
    username = CASClient().authenticate()
    deliv = Deliverer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()

    id = request.args.get('details_id')
    order = Order.query.filter_by(id=id).first()
    cust = Customer.query.filter_by(id=order.custid).first()
    orderitems = OrderItem.query.filter_by(Order=order)

    # out_of_stock_id = request.args.get('out_of_stock_id')
    # if out_of_stock_id is not None:
    #     item 

    item_info = []
    for orderitem in orderitems:

        item = Item.query.filter_by(id=orderitem.itemid).first()
        total_price = item.price * orderitem.quantity

        item_info.append({
            "name": item.name,
            "total_price": total_price,
            "price": item.price,
            "quantity": orderitem.quantity,
        })

    order_info = []
    order_info.append({
        "status": order.status,
        "building": order.building,
        "roomnum": order.roomnum,
        "note": order.note,
        "price": order.price,
        "time_placed": order.time_placed,
    })

    cust_info = []
    cust_info.append({
        "name": cust.name,
        "phone_number": cust.phone_number,
        "email": cust.email,
    })

    return render_template('orderdetails.html', item_info=item_info, order_info=order_info, cust_info=cust_info)

from app import app, db, mail
from database import Customer, Deliverer, CartItem, Order, OrderItem, Item
from flask import render_template, request, make_response, redirect, url_for
from flask_mail import Message
from flask_sslify import SSLify
from CASClient import CASClient
from datetime import datetime
import stripe
import urllib
import os 
import re

PHONE_REGEXP = "^[0-9]{10}$|^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
VENMO_REGEXP = "@.*"

BEING_DELIVERED = "Being Delivered"
DELIVERED = "Delivered"
WAITING = "Waiting for Deliverer"

categories = ['All', 'Food', 'Kitchenware', 'Medicine', 'Toiletries', 'Cleaning Supplies']

sslify = SSLify(app)
admin_mail = os.environ.get('MAIL_USERNAME')

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
    venmo = request.args.get('venmo')

    if not fname and not lname and not phone and not venmo:
        return render_template('createaccount.html', errorMsg="")
    elif not fname or not lname or not phone or not venmo:
        return render_template('createaccount.html', errorMsg="Missing first/last name, phone and/or venmo.")
    elif not re.search(VENMO_REGEXP, venmo):
        return render_template('createaccount.html', errorMsg="Invalid venmo. Venmo must start with the '@' character.")
    elif not re.search(PHONE_REGEXP, phone):
        return render_template('createaccount.html', errorMsg="Invalid phone number. Number must be US number of the form xxx-xxx-xxxx")

    newcust = Customer(
        first_name=fname,
        last_name=lname,
        phone_number=phone, 
        venmo=venmo,
        email=str(username.strip() + "@princeton.edu"))
    newdeliv = Deliverer(
        first_name=fname,
        last_name=lname,
        phone_number=phone, 
        email=str(username.strip() + "@princeton.edu"),
        venmo=venmo,
        balance=0)
    
    db.session.add(newcust)
    db.session.add(newdeliv)
    db.session.commit()

    return render_template('index.html')

@app.route("/homecustomer")
def homecustomer():

    username = CASClient().authenticate()
        
    query = request.args.get('query')
    # check the arguments, and then cookies for the category
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
            "in_stock": item.inStock,
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
        item.quantity = int(quant)
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
        cust = order.Customer
        total = '%.2f'%(order.price)
        results.append({
            "id": order.id,
            "name": "%s %s" % (cust.first_name, cust.last_name),
            "phone_number": cust.phone_number,
            "building": order.building,
            "roomnum": order.roomnum,
            "price": total,
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
            "name": "%s %s" % (order.Customer.first_name, order.Customer.last_name),
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

    # change item quantity within cart (same as /homecustomer route)
    itemid = request.args.get('added')
    if itemid is not None:
        item = CartItem.query.filter_by(Customer=cust, itemid=itemid).first()
        quant = request.args.get('quantity')
        if quant is not None:
            item.quantity = int(quant)
            db.session.commit()

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

        fee = max(1.99, 0.17 * subtotal)
    
    total = '%.2f'%(subtotal + fee)
    subtotal = '%.2f'%(subtotal)
    fee = '%.2f'%(fee)

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
    stripe.api_key = os.environ.get('SECRET_KEY')

    total = request.args.get('total')
    building = request.args.get('building')
    roomnum = request.args.get('roomnum')
    note = request.args.get('note')

    print('The total is: ' + str(int(float(total) * 100)))
    print()
    print()
    print()

    # for testing payments when debugging
    total = 0.50
    session = stripe.checkout.Session.create(
    customer_email=str(username.strip() + '@princeton.edu'),
    payment_method_types=['card'],
    line_items=[{
        'name': 'Confirm Order',
        'description': '''We will get these items to you in a jif! 
        For testing you will be charged $0.50''',
        'images': ['https://pbs.twimg.com/profile_images/685549530771800064/dR3EZHkC_400x400.png'],
        'amount': int(float(total) * 100),
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

        fee = max(1.99, 0.17 * subtotal)
    
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

            deliverer = delivered.Deliverer
            if deliverer:
                deliverer.balance += delivered.price
            
            db.session.add(deliverer)
            db.session.commit()

    orders = Order.query.filter_by(Customer=cust).all()
    result = []
    for order in orders:
        
        if order.Deliverer is None:
            deliverer = "None"
        else:
            deliverer = "%s %s" % (order.Deliverer.first_name, order.Deliverer.last_name)
        result.append({
            "id": order.id,
            "customer": "%s %s" % (order.Customer.first_name, order.Customer.last_name),
            "deliverer": deliverer,
            "status": order.status,
        })


    msg = Message("Order Placed!",
        sender=admin_mail,
        recipients=[cust.email])
    msg.body = "Hello!\n\nYour order with TigerTask has been placed! Stay tuned for more updates. "
    msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
    msg.body += "\n\nBest,\nTigerTask Team "
    mail.send(msg)

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

        cust = order.Customer

        msg = Message("Order Claimed!",
            sender=admin_mail,
            recipients=[cust.email])
        msg.body = "Hello!\n\nGood news! Your order has been claimed. Your deliverer is "
        msg.body += deliv.first_name + " " + deliv.last_name + " and their phone number is " + deliv.phone_number + "."
        msg.body += "\n\nOnce your order is delivered, make sure to confirm it under the 'Orders' page on tigertask.herokuapp.com."
        msg.body += "\n\nBest,\nTigerTask Team"
        mail.send(msg)

    return redirect(url_for('deliveries'))

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

            # we need to add this balance to the deliverer's account
            deliverer = delivered.Deliverer
            deliverer.balance += delivered.price

            db.session.commit()

            # send an email noting successful delivery
            msg = Message("Order Delivered!",
                sender=admin_mail,
                recipients=[customer.email])
            msg.body = "Thank you for using TigerTask!"
            msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
            msg.body += "\n\nBest,\nTigerTask Team "
            mail.send(msg)

            msg = Message("Order Delivered!",
                sender=admin_mail,
                recipients=[deliverer.email])
            msg.body = "Your customer marked his item as delivered. Thank your for your work!"
            msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
            msg.body += "\n\nBest,\nTigerTask Team"
            mail.send(msg)

    canceled = request.args.get('canceled')
    if canceled is not None:
        removed_order = Order.query.filter_by(id=canceled).first()

        msg = Message("Cancellation Requested",
                sender=admin_mail,
                recipients=[admin_mail])
        msg.body = "A customer has requested a cancellation to their order.\n\n"
        msg.body += "Venmo: " + customer.venmo + "\n"
        msg.body += "Amount: " + removed_order.price
        mail.send(msg)

        msg = Message("Order Cancelled",
                sender=admin_mail,
                recipients=[customer.email])
        msg.body = "Hello!"
        msg.body += "\n\nYour TigerTask order has been cancelled. You should expect to receive a venmo refund within the next 24 hours."
        msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
        msg.body += "\n\nBest,\nTigerTask Team"
        mail.send(msg)

        if removed_order is not None:
            print("removing order")
            canceled_order_items = OrderItem.query.filter_by(Order=removed_order).all()
            for item in canceled_order_items:
                db.session.delete(item)
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
            deliverer_name = "%s %s" % (order.Deliverer.first_name, order.Deliverer.last_name)
            deliverer_num = order.Deliverer.phone_number
        result.append({
            "id": order.id,
            "customer": "%s %s" % (order.Customer.first_name, order.Customer.last_name),
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

     # orderitem id of an item that is being marked out of stock
    out_of_stock_id = request.args.get('out_of_stock_id')
    if out_of_stock_id is not None:
        orderitem = OrderItem.query.get(out_of_stock_id)
        item = orderitem.Item
        total_price = orderitem.quantity * item.price

        i = 0
        for orderitem in orderitems:
            i += 1

        if i == 1:
            msg = Message("Item Out of Stock",
                    sender=admin_mail,
                    recipients=[cust.email])
            msg.body = "Hello!"
            msg.body += "\n\nUnfortunately, the item that you purchased is out of stock."
            msg.body += "\n\nItem Name: " + item.name
            msg.body += "\nQuantity: " + str(orderitem.quantity)
            msg.body += "\nOrder Total: " + str(order.price)
            msg.body += "\n\nYou will receive a Venmo refund for the full amount of this order within 24 hours. We apologize sincerely for this inconvenience."
            msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
            msg.body += "\n\nBest,\nTigerTask Team"
            mail.send(msg)

            msg = Message("Item Out of Stock - Order Cancelled",
                    sender=admin_mail,
                    recipients=[admin_mail])
            msg.body = "A customer has an item out of stock, and their order was cancelled."
            msg.body += "\n\nVenmo: " + cust.venmo
            msg.body += "\nAmount: " + str(order.price)
            mail.send(msg)

            orderitem.Item.inStock = "False" 
            db.session.delete(orderitem)
            db.session.delete(order)
            db.session.commit()

            return redirect(url_for('homedeliver'))

        else:
            msg = Message("Item Out of Stock",
                    sender=admin_mail,
                    recipients=[cust.email])
            msg.body = "Hello!"
            msg.body += "\n\nUnfortunately, one of the items you ordered is out of stock."
            msg.body += "\n\nItem Name: " + item.name
            msg.body += "\nQuantity: " + str(orderitem.quantity)
            msg.body += "\nTotal Price: " + str(total_price)
            msg.body += "\n\nYou will receive a Venmo refund with the amount paid for this item within 24 hours. The rest of your order is still on the way. We apologize for the inconvenience!"
            msg.body += "\n\nIf you have any questions, feel free to email us at tigertask.princeton@gmail.com."
            msg.body += "\n\nBest,\nTigerTask Team"
            mail.send(msg)

            msg = Message("Item Out of Stock",
                    sender=admin_mail,
                    recipients=[admin_mail])
            msg.body = "A customer has an item out of stock."
            msg.body += "\n\nVenmo: " + cust.venmo
            msg.body += "\nAmount: " + str(total_price)
            mail.send(msg)

            orderitem.Item.inStock = "False"
            order.price = order.price - total_price
            db.session.delete(orderitem)
            db.session.commit()

     # orderitem id of an item that is being marked out of stock
    in_stock_id = request.args.get('in_stock_id')
    if in_stock_id is not None:
       orderItem = OrderItem.query.get(in_stock_id)
       if orderItem:
           orderItem.Item.inStock = "True" 
           db.session.commit()

    item_info = []
    subtotal = 0
    for orderitem in orderitems:

        item = orderitem.Item #Item.query.filter_by(id=orderitem.itemid).first()

        item_info.append({
            "id": orderitem.id,
            "name": item.name,
            "price": item.price,
            "quantity": orderitem.quantity,
            "in_stock": item.inStock,
        })
        subtotal += item.price * orderitem.quantity

    deliverer_fee = '%.2f'%(order.price - subtotal)
    subtotal = '%.2f'%(subtotal)
    total = '%.2f'%(order.price)
    
    order_info = {
        "id": order.id,
        "status": order.status,
        "building": order.building,
        "roomnum": order.roomnum,
        "note": order.note,
        "price": total,
        "time_placed": order.time_placed,
        "deliverer_first_name": deliv.first_name,
        "deliverer_last_name": deliv.last_name,
    }

    cust_info = []
    cust_info.append({
        "first_name": cust.first_name,
        "last_name": cust.last_name,
        "phone_number": cust.phone_number,
        "email": cust.email,
    })

    return render_template('orderdetails.html', subtotal = subtotal, deliverer_fee = deliverer_fee, total = total, item_info=item_info, order=order_info, cust_info=cust_info)


@app.route("/dashboard")
def dashboard():
    username = CASClient().authenticate()
    deliverer = Deliverer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()
    customer = Customer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()

    message = ""

    # get the phone number if edited
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone')
    venmo = request.args.get('venmo')
    if first_name and last_name and phone_number and venmo:

        if not re.search(VENMO_REGEXP, venmo):
            return render_template('dashboard.html',message="", person=deliverer, error="Failed to update profile. Venmo must start with the '@' character.")
        elif not re.search(PHONE_REGEXP, phone_number):
           return render_template('dashboard.html',message="", person=deliverer, error="Failed to update profile. Please provide a US number of the form xxx-xxx-xxxx")

        # update customer table
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone_number = phone_number
        customer.venmo = venmo
        
        # update deliverer table
        deliverer.first_name = first_name
        deliverer.last_name = last_name
        deliverer.phone_number = phone_number
        deliverer.venmo = venmo

        # save 
        db.session.add(deliverer)
        db.session.add(customer)
        db.session.commit()
        message = "Your profile has been updated."

    return render_template('dashboard.html',message=message, person=deliverer, error="")

@app.route("/account")
def account():
    username = CASClient().authenticate()
    deliverer = Deliverer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()
    customer = Customer.query.filter_by(email=str(username.strip()+"@princeton.edu")).first()

    message = ""

    # get the phone number if edited
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone')
    venmo = request.args.get('venmo')
    if first_name and last_name and phone_number and venmo:

        if not re.search(VENMO_REGEXP, venmo):
            return render_template('account.html',message="", person=customer, error="Failed to update profile. Venmo must start with the '@' character.")
        elif not re.search(PHONE_REGEXP, phone_number):
            return render_template('account.html',message="", person=customer, error="Failed to update profile. Please provide a US number of the form xxx-xxx-xxxx")

        # update customer table
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone_number = phone_number
        customer.venmo = venmo
        
        # update deliverer table
        deliverer.first_name = first_name
        deliverer.last_name = last_name
        deliverer.phone_number = phone_number
        deliverer.venmo = venmo

        # save 
        db.session.add(deliverer)
        db.session.add(customer)
        db.session.commit()
        message = "Your profile has been updated."

    return render_template('account.html',message=message, person=customer, error="")

@app.route('/helpcustomer')
def helpcustomer():
    return render_template('helpcustomer.html')

@app.route('/helpdeliver')
def helpdeliver():
    return render_template('helpdeliver.html')
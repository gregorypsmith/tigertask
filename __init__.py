import os

from routes import app
import routes
from database import Customer, Deliverer, Item, Order, CartItem, OrderItem, db

if __name__ == "__main__":
    app.run(debug=True)
import sqlite3
from files.models import Buyer
from files import db
from files.config import PRODUCT_DATABASE, get_cursor
from flask_login import current_user

def db_query(query, data):
    dbAddress = PRODUCT_DATABASE
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()

def update_status(data):
    query = "UPDATE orders SET status = ? WHERE id = ?"
    db_query(query, data)

def place_order(data):
    query = "INSERT INTO orders (productID, buyerID, sellerID, buyerName, buyerEmail) VALUES (?, ?, ?, ?, ?)"
    db_query(query, data)


def add_to_cart(data):
    query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
    db_query(query, data)

def delete_from_cart(data):
    query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
    db_query(query, data)

def add_to_wishlist(data):
    query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
    db_query(query, data)

def delete_from_wishlist(data):
    query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
    db_query(query, data)


def add_buyer(form_data):
    newBuyer = Buyer(fname = form_data.buyerFirstName.data,\
                    lname = form_data.buyerLastName.data,\
                    email = form_data.email.data,\
                    password = form_data.pswd.data,\
                    address = form_data.address.data,\
                    city = form_data.city.data,\
                    state = form_data.state.data,\
                    pin = form_data.pin.data)
    db.session.add(newBuyer)
    db.session.commit()

def get_products_details():
    cursor = get_cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "seller_id" : result[7],
            "prod_seller" : result[8]
        })
    return prods


def get_wish_details():
    connection = sqlite3.connect(PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM products \
            INNER JOIN basket ON basket.productID = products.id\
            WHERE basket.buyerID = (?) AND basket.btype = 'w'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "seller_id" : result[7],
            "prod_seller" : result[8]
        })
    return prods

    
def get_cart_details():
    connection = sqlite3.connect(PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM products \
            INNER JOIN basket ON basket.productID = products.id \
            WHERE basket.buyerID = (?) AND basket.bType = 'c'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "seller_id" : result[7],
            "prod_seller" : result[8]
        })
    return prods


def get_order_details():
    connection = sqlite3.connect(PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM products \
            INNER JOIN orders ON orders.productID = products.id \
            WHERE orders.buyerID = (?) AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "seller_id" : result[7],
            "prod_seller" : result[8],
            "order_id": result[9],
            "order_status" : result[15]
        })
    return prods


def get_history_details():
    connection = sqlite3.connect(PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN \
            orders ON orders.productID = products.id \
            WHERE orders.buyerID = (?) AND (orders.status = 'Received' OR orders.status = 'Cancelled')"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "prod_seller" : result[8],
            "order_id": result[9],
            "order_status" : result[15]
        })
    return prods


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
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def update_status(action):
    query = "UPDATE orders SET status = ? WHERE id = ?"
    data = data = (str(action[1]), int(action[2]), )
    db_query(query, data)


def place_order(action):
    if len(action) == 2:
        place_bulk_order(action[1])
    else:
        data = (int(action[1]), int(current_user.id), int(action[2]), current_user.fname, current_user.email, ) 
        query = "INSERT INTO orders (productID, buyerID, sellerID, buyerName, buyerEmail) VALUES (?, ?, ?, ?, ?)"
        db_query(query, data)
        query = """ DELETE FROM basket
                    WHERE productID = ? AND buyerID = ? AND 
                    EXISTS(SELECT 1 FROM basket WHERE productID = ? AND buyerID = ? LIMIT 1) """
        data = (int(action[1]), int(current_user.id), int(action[1]), int(current_user.id), )
        db_query(query, data)


def place_bulk_order(bType):
    print("\n\n\n")
    query = "SELECT productID FROM basket WHERE buyerID = ? AND bType = ?"
    data = (int(current_user.id), str(bType), ) 
    results = db_query(query, data)
    actions = []
    query = "SELECT id, sellerID FROM products WHERE id = ?"
    for result in results:
        res = db_query(query, (int(result[0]), ))
        actions.append((-1, res[0][0], res[0][1]))
    print(actions)
    print("\n\n\n")
    for action in actions:
        place_order(action)


def add_to_cart(action):
    if len(action) == 1:
        add_all_to_cart()
    else:
        query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
        data = (int(action[1]), int(current_user.id), "c", ) 
        db_query(query, data)


def add_all_to_cart():
    query = """ UPDATE basket SET bType = 'c' WHERE buyerID = ? """
    data = (int(current_user.id), )     
    db_query(query, data)


def delete_from_cart(action):
    if len(action) == 1:
        query = "DELETE FROM basket WHERE buyerID = ?"
        data = (int(current_user.id), ) 
    else:
        query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
        data = (int(action[1]), int(current_user.id), ) 
    db_query(query, data)


def add_to_wishlist(action):
    if len(action) == 1:
        add_all_to_wishlist()
    else:        
        query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
        data = (int(action[1]), int(current_user.id), "w", )     
        db_query(query, data)

def add_all_to_wishlist():
    query = """ UPDATE basket SET bType = 'w' WHERE buyerID = ? """
    data = (int(current_user.id), )     
    db_query(query, data)


def delete_from_wishlist(action):
    if len(action) == 1:
        query = "DELETE FROM basket WHERE buyerID = ?"
        data = (int(current_user.id), ) 
    else:
        query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
        data = (int(action[1]), int(current_user.id), ) 
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


def get_this_product(data):
    cursor = get_cursor()
    print(type(data))
    data = "%{}%".format(data)
    query = "SELECT * FROM products\
            WHERE \
            (ProductName LIKE '{}') OR\
            (productType LIKE '{}') OR\
            (productDesc LIKE '{}') OR\
            (shopName LIKE '{}') OR\
            (sellerAddress LIKE '{}')\
            ORDER BY productName, productType, shopName, sellerAddress, productDesc"\
            .format(data, data, data, data, data)
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


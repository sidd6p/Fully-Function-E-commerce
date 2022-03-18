import pyodbc
from files.models import Buyer
from files import db, config
from flask_login import current_user
from datetime import datetime



################# DB Query #################
def dbquery(query, data, type = 'N'):
    connection = pyodbc.connect('DRIVER='+config.PRODUCT_DRIVER+';SERVER=tcp:'+config.PRODUCT_SERVER+';PORT=1433;DATABASE='+config.PRODUCT_DATABASE+';UID='+config.PRODUCT_USER+';PWD='+ config.PRODUCT_PSWD)
    cursor = connection.cursor()
    result = []
    if len(data) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    if type == 'S':
        result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


################# Update Order Status #################
def update_status(action):
    query = "UPDATE orders SET status = ? WHERE id = ?"
    data = data = (str(action[1]), int(action[2]), )
    dbquery(query, data)


################# Place Order #################
def place_order(action, quantity):
    if len(action) == 2:
        place_bulk_order(action[1])
    else:
        buyer_address = current_user.address + " " + current_user.city + " " + current_user.state + " " + str(current_user.pin)
        data = (int(action[1]), int(current_user.id), int(action[2]), current_user.fname, current_user.email, datetime.utcnow(),buyer_address, quantity ) 
        query = "INSERT INTO orders (productID, buyerID, sellerID, buyerName, buyerEmail, orderTime, buyeAdd, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        dbquery(query, data)
        query = """ DELETE FROM basket
                    WHERE productID = ? AND buyerID = ? AND 
                    EXISTS(SELECT TOP 1 * FROM basket WHERE productID = ? AND buyerID = ?) """
        data = (int(action[1]), int(current_user.id), int(action[1]), int(current_user.id), )
        dbquery(query, data)


################# Place Bulk Order #################
def place_bulk_order(bType):
    query = "SELECT productID FROM basket WHERE buyerID = ? AND bType = ?"
    data = (int(current_user.id), str(bType), ) 
    results = dbquery(query, data, 'S')
    actions = []
    query = "SELECT id, sellerID FROM products WHERE id = ?"
    for result in results:
        res = dbquery(query, (int(result[0]), ), 'S')
        actions.append((-1, res[0][0], res[0][1]))
    for action in actions:
        place_order(action, 1)


################# Cart #################
def get_cart_details():
    query = "SELECT * FROM products \
            INNER JOIN basket ON basket.productID = products.id \
            WHERE basket.buyerID = (?) AND basket.bType = 'c'"
    data = (int(current_user.id), )
    results = dbquery(query, data, 'S')
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "seller_add" : result[6],
            "prod_shop": result[7],
            "seller_email" : result[8],
            "seller_id" : result[9],
        })
    return prods


################# Add to Cart #################
def add_to_cart(action):
    if len(action[1]) == 1 and action[1] == 'c':
        add_all_to_cart()
    else:
        query = """ DELETE FROM basket WHERE productID = ? AND buyerID = ? """
        data = (int(action[1]), int(current_user.id), )
        dbquery(query, data)
        query = """ INSERT into basket (productID, buyerID, bType) VALUES (?, ?, ?)  """
        type = "c"
        data = (int(action[1]), int(current_user.id), str(type), ) 
        dbquery(query, data)


################# Add ALl to Cart #################
def add_all_to_cart():
    query = """ UPDATE basket SET bType = 'c' WHERE buyerID = ? """
    data = (int(current_user.id), )     
    dbquery(query, data)


################# Delete from Cart #################
def delete_from_cart(action):
    if len(action) == 1:
        query = "DELETE FROM basket WHERE buyerID = ? AND bType = 'c'"
        data = (int(current_user.id), ) 
    else:
        query = "DELETE FROM basket WHERE productID = ? AND buyerID = ? AND bType = 'c'"
        data = (int(action[1]), int(current_user.id), ) 
    dbquery(query, data)


################# Wishlist #################
def get_wish_details():
    query = "SELECT * FROM products \
            INNER JOIN basket ON basket.productID = products.id\
            WHERE basket.buyerID = (?) AND basket.btype = 'w'"
    data = (int(current_user.id), )
    results = dbquery(query, data, 'S')
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "seller_add" : result[6],
            "prod_shop": result[7],
            "seller_email" : result[8],
            "seller_id" : result[9],
        })
    return prods


################# Add to Wishlist #################
def add_to_wishlist(action):
    if len(action[1]) == 1 and action[1] == 'w':
        add_all_to_wishlist()
    else:
        query = """ DELETE FROM basket WHERE productID = ? AND buyerID = ? """
        data = (int(action[1]), int(current_user.id), )
        dbquery(query, data)
        query = """ INSERT into basket (productID, buyerID, bType) VALUES (?, ?, ?)  """
        type = "w"
        data = (int(action[1]), int(current_user.id), str(type), ) 
        dbquery(query, data)


################# Add All to Wishlist #################
def add_all_to_wishlist():
    print("Adding ALLL to wishlist\n\n\n\n")
    query = """ UPDATE basket SET bType = 'w' WHERE buyerID = ? """
    data = (int(current_user.id), )     
    dbquery(query, data)


################# Delete from Wishlist #################
def delete_from_wishlist(action):
    if len(action) == 1:
        query = "DELETE FROM basket WHERE buyerID = ? AND bType = 'w'"
        data = (int(current_user.id), ) 
    else:
        query = "DELETE FROM basket WHERE productID = ? AND buyerID = ? AND bType = 'w'"
        data = (int(action[1]), int(current_user.id), ) 
    dbquery(query, data)

    
################# Orders #################
def get_order_details():
    query = "SELECT * FROM products \
            INNER JOIN orders ON orders.productID = products.id \
            WHERE orders.buyerID = (?) AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    results = dbquery(query, data, 'S')
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "seller_add" : result[6],
            "prod_shop": result[7],
            "seller_email" : result[8],
            "seller_id" : result[9],
            "order_id": result[10],
            "order_status" : result[16],
            "order_quantity" : result[19]
        })
    return prods


################# History #################
def get_history_details():
    query = "SELECT * FROM products INNER JOIN \
            orders ON orders.productID = products.id \
            WHERE orders.buyerID = (?) AND (orders.status = 'Received' OR orders.status = 'Cancelled')"
    data = (int(current_user.id), )
    results = dbquery(query, data, 'S')
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "seller_add": result[6],
            "prod_shop": result[7],
            "seller_email" : result[8],
            "order_id": result[10],
            "order_status" : result[16],
            "order_quantity": result[19]
        })
    return prods



################# Verify Hash Password #################
def verify_pswd(plain_pswd, hased_pswd):
    return config.PSWD_CONTEXT.verify(plain_pswd, hased_pswd)
    

################# Add Buyer #################
def add_buyer(form_data):
    newBuyer = Buyer(fname = form_data.buyerFirstName.data,\
                    lname = form_data.buyerLastName.data,\
                    email = form_data.email.data,\
                    password = config.PSWD_CONTEXT.hash(form_data.pswd.data),\
                    address = form_data.address.data,\
                    city = form_data.city.data,\
                    state = form_data.state.data,\
                    pin = form_data.pin.data)
    db.session.add(newBuyer)
    db.session.commit()


################# Product Details #################
def get_products_details():
    if (current_user.is_authenticated):
        query = "SELECT * FROM products where sellerPin = (?)"
        data = (current_user.pin, )
    else:
        query = "SELECT * FROM products"
        data = ()
    results = dbquery(query, data, 'S')
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "seller_add" : result[6],
            "prod_shop": result[7],
            "seller_email" : result[8],
            "seller_id" : result[9],
        })
    return prods


################# Product Search #################
def get_this_product(data):
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
    data = ()
    results = dbquery(query, data, 'S')
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


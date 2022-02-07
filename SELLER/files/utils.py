import secrets
import os
import pyodbc
from .models import Seller
from files import db, config
from flask_login import current_user



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


################# Save Image #################
def saveImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    return imageName


################# Verify Hash Password #################
def verify_pswd(plain_pswd, hased_pswd):
    return config.PSWD_CONTEXT.verify(plain_pswd, hased_pswd)
    

################# Add Seller #################
def add_seller(form):
    shopLogo = saveImage(form.shopLogo.data)
    new_seller = Seller(
                        fname = form.sellerFirstName.data,\
                        lname = form.sellerLastName.data,\
                        email = form.email.data,\
                        password = config.PSWD_CONTEXT.hash(form.pswd.data),\
                        address = form.address.data,\
                        city = form.city.data, \
                        state = form.state.data, \
                        pin = form.pin.data, \
                        shopName= form.shopName.data, \
                        shopLogo = get_image_url(shopLogo)
                        )
    db.session.add(new_seller)
    db.session.commit()


################# Add Product #################
def add_product(form):
    productImage = saveImage(form.productPhoto.data)
    query = """ INSERT INTO products 
                (productName, 
                productType, 
                productPhoto, 
                productDesc, 
                productPrice, 
                shopName, 
                sellerID, 
                sellerAddress,
                sellerEmail)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """
    data =  (
            form.productName.data,\
            form.productType.data,\
            get_image_url(productImage),\
            form.productDesc.data,\
            int(form.productPrice.data),\
            current_user.shopName,\
            int(current_user.id),\
            current_user.address,\
            current_user.email,\
            )
    dbquery(query, data)


################# Image Url #################
def get_image_url(image_name):
    container_client = config.get_client()
    logo_url = container_client.get_blob_client(blob = image_name).url
    return logo_url


################# Product Details #################
def get_products_details(current_user_id: int):
    query = "SELECT * FROM products WHERE sellerID = (?)"
    data = (current_user_id, )
    results = dbquery(query, data, "S")
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],

        })
    return prods


################# Product Search #################
def get_this_product(current_user_id: int, data):
    data = "%{0}%".format(data)
    query = "SELECT * FROM products\
            WHERE\
            (sellerID = {}) AND (\
            ProductName LIKE '{}' OR\
            productType LIKE '{}' OR\
            productDesc LIKE '{}')\
            ORDER BY productName, productType, productDesc"\
            .format(current_user_id, data, data, data, data, data)
    data = ()
    results = dbquery(query, data, "S")
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


################# Update Order Status #################
def update_order_status(action):
    query = " UPDATE orders SET status = ? WHERE id = ?"
    data = (str(action[0]), int(action[1]),)
    dbquery(query, data)


################# Order #################
def get_all_orders():
    query = "SELECT \
                products.productName, \
                products.productPhoto, \
                orders.buyerName, \
                orders.buyerEmail,\
                orders.id,\
                orders.status,\
                orders.productID,\
                orders.orderTime,\
                orders.buyeAdd\
            FROM products INNER JOIN orders ON products.sellerID = orders.sellerID\
            WHERE orders.sellerID = (?) AND orders.productID = products.id AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    results = dbquery(query, data, "S")
    orders = []
    for result in results:
        orders.append({
                    "productName" : result[0],
                    "productPhoto" : result[1],
                    "buyerName" : result[2],
                    "buyerEmail" : result[3],
                    "orderId" : result[4],
                    "status" : result[5],
                    "productID" : result[6],
                    "orderTime" : result[7],
                    "buyerAdd" : result[8]
                    })
    return orders


################# History #################
def get_orders_history():
    query = "SELECT \
                products.productName, \
                products.productPhoto, \
                orders.buyerName, \
                orders.buyerEmail,\
                orders.id,\
                orders.status,\
                orders.productID,\
                orders.orderTime,\
                orders.buyeAdd\
            FROM products INNER JOIN orders ON products.sellerID = orders.sellerID\
            WHERE orders.sellerID = (?) AND orders.productID = products.id AND orders.status = 'Received' OR orders.status = 'Cancelled'"
    data = (int(current_user.id), )
    results = dbquery(query, data, "S")
    orders = []
    for result in results:
        orders.append({
                    "productName" : result[0],
                    "productPhoto" : result[1],
                    "buyerName" : result[2],
                    "buyerEmail" : result[3],
                    "orderId" : result[4],
                    "status" : result[5],
                    "productID" : result[6],
                    "orderTime" : result[7],
                    "buyerAdd" : result[8]
                    })
    return orders
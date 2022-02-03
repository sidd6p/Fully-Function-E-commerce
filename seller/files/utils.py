import sqlite3
import secrets
import os
from .models import Seller
from files import db, config
from flask_login import current_user


def dbquery(query, data):
    dbAddress = config.PROD_DB
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()

def saveProdImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    return imageName

def saveShopImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    return imageName


def add_seller(form):
    shopLogo = saveShopImage(form.shopLogo.data)
    new_seller = Seller(fname = form.sellerFirstName.data,\
                    lname = form.sellerLastName.data,\
                    email = form.email.data,\
                    password = form.pswd.data,\
                    address = form.address.data,\
                    city = form.city.data, \
                    state = form.state.data, \
                    pin = form.pin.data, \
                    shopName= form.shopName.data, \
                    shopLogo = get_image_url(shopLogo))
    db.session.add(new_seller)
    db.session.commit()


def add_product(form):
    productImage = saveProdImage(form.productPhoto.data)
    connection = sqlite3.connect(config.PROD_DB)
    cursor = connection.cursor()
    query = """ INSERT INTO products 
                (productName, 
                productType, 
                productPhoto, 
                productDesc, 
                productPrice, 
                shopName, 
                sellerID, 
                sellerAddress)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?) """
    data =  (form.productName.data, form.productType.data, get_image_url(productImage), form.productDesc.data, int(form.productPrice.data), current_user.shopName, int(current_user.id), current_user.address, )
    cursor.execute(query, data)
    connection.commit()
    connection.close()


def get_image_url(image_name):
    container_client = config.get_client()
    logo_url = container_client.get_blob_client(blob = image_name).url
    return logo_url

def get_products_details(current_user_id: int):
    cursor = config.get_cursor()
    query = "SELECT * FROM products WHERE sellerID = (?)"
    data = (current_user_id, )
    cursor.execute(query, data)
    results = cursor.fetchall()
    print(results)
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

        # productImage = saveProdImage(form.productPhoto.data)
        # connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO products (productName, productType, productPhoto, productDesc, productPrice, shopName, sellerID, sellerAddress) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # data =  (form.productName.data, form.productType.data, productImage, form.productDesc.data, int(form.productPrice.data), current_user.shopName, int(current_user.id), current_user.address, )
        # cursor.execute(query, data)
        # connection.commit()
        # connection.close()
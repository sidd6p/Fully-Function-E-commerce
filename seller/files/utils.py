import sqlite3
import secrets
import os
from PIL import Image
from .models import Seller
from files import db, config

def dbquery(query, data):
    dbAddress = r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db'
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

prodDirPath = r"C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\images\products"

def saveShopImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    # imagePath = os.path.join(current_app.root_path, 'static\images\shops', imageName)
    # outputSize = (255, 255)
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    # i = Image.open(formImage)
    # i.thumbnail(outputSize)
    # i.save(imagePath)
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
                    shopLogo = shopLogo)
    db.session.add(new_seller)
    db.session.commit()

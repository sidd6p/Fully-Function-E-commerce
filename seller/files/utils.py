import sqlite3
import secrets
import os
from PIL import Image
from .models import Seller
from files import db, config
import io

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
                    shopLogo = shopLogo)
    db.session.add(new_seller)
    db.session.commit()


def get_logo_url(logo_name):
    container_client = config.get_client()
    logo_url = container_client.get_blob_client(blob = logo_name).url
    return logo_url

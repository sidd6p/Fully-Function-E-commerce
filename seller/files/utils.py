import sqlite3
import secrets
import os
from flask import current_app
from PIL import Image

def dbquery(query, data):
    dbAddress = r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db'
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()

def saveShopImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    imagePath = os.path.join(current_app.root_path, 'static\images\shops', imageName)
    outputSize = (255, 255)
    i = Image.open(formImage)
    i.thumbnail(outputSize)
    i.save(imagePath)
    return imageName
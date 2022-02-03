import os

class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_BINDS = {
        'sellerdb' : "sqlite:///databases/seller.db",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # UPLOAD_FOLDER = "C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\images\products"

import os

class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_BINDS = {
        'buyerdb' : "sqlite:///databases/buyer.db",
        'sellerdb' : "sqlite:///databases/seller.db",
        'productdb' : "sqlite:///databases/product.db"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

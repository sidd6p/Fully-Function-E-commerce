import os

DB_ADDRESS = r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db'
class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_BINDS = {
        'buyerdb' : "sqlite:///databases/buyer.db",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


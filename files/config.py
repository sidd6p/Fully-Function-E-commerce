import os

class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

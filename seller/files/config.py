import os
from azure.storage.blob import BlobServiceClient
import sqlite3


PROD_DB = r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db'

class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_BINDS = {
        'sellerdb' : "sqlite:///databases/seller.db",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def get_client():
    conn_str = "DefaultEndpointsProtocol=https;AccountName=learn10sg;AccountKey=AHTtAU6SOIzK7jqLwgyVm88BTyqNgduQkc6jPXj30RWgPOAh7TGzdTGYfKxSSlU1mq9a9H/14ZltDPJJMSfxJQ==;EndpointSuffix=core.windows.net" # retrieve the connection string from the environment variable
    container = "cnt1"
    blob_service_client = BlobServiceClient.from_connection_string(conn_str = conn_str)
    container_service_client = blob_service_client.get_container_client(container=container)
    container_service_client.get_container_properties()
    return container_service_client

def get_cursor():
    connection = sqlite3.connect(PROD_DB)
    cursor = connection.cursor()
    return cursor
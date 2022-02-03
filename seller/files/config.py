from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import sqlite3
import os



load_dotenv()



PRODUCT_DATABASE = os.getenv(r'PRODUCT_DATABASE')
SELLER_DATABASE = os.getenv('SELLER_DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
CONNECTION_STRING = os.getenv('CONNECT_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')



class Config(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_BINDS = {
        'sellerdb' : SELLER_DATABASE,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_client():
    conn_str = CONNECTION_STRING
    container = CONTAINER_NAME
    blob_service_client = BlobServiceClient.from_connection_string(conn_str = conn_str)
    container_service_client = blob_service_client.get_container_client(container=container)
    container_service_client.get_container_properties()
    return container_service_client


def get_cursor():
    connection = sqlite3.connect(PRODUCT_DATABASE)
    cursor = connection.cursor()
    return cursor
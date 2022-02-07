from azure.storage.blob import BlobServiceClient
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


PSWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()



PRODUCT_DATABASE = os.getenv(r'PRODUCT_DATABASE')
SELLER_DATABASE = os.getenv('SELLER_DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
CONNECTION_STRING = os.getenv('CONNECT_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')
PRODUCT_SERVER = os.getenv('PRODUCT_SERVER')  
PRODUCT_DATABASE = os.getenv('PRODUCT_DATABASE') 
PRODUCT_USER = os.getenv('PRODUCT_USER') 
PRODUCT_PSWD = os.getenv('PRODUCT_PSWD') 
PRODUCT_DRIVER = os.getenv('PRODUCT_DRIVER') 


class Config(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_BINDS = {
        'sellerdb' : SELLER_DATABASE,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_client():
    blob_service_client = BlobServiceClient.from_connection_string(conn_str = CONNECTION_STRING)
    container_service_client = blob_service_client.get_container_client(container=CONTAINER_NAME)
    container_service_client.get_container_properties()
    return container_service_client

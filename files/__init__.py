from flask import Flask
from files.config import Config
from files.buyer.routes import buyer
from files.seller.routes import seller
from files.general.routes import general

def createApp(congigClass = Config):
    app = Flask(__name__)
    app.config.from_object(congigClass)

    app.register_blueprint(buyer)
    app.register_blueprint(seller)
    app.register_blueprint(general)
    
    return app
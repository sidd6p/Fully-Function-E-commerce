from flask import Flask
from files.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
loginManager = LoginManager()
loginManager.login_view = 'user.login'
loginManager.login_message = "You need to Log-In first"
loginManager.login_message_category = 'warning'

def createApp(congigClass = Config):
    app = Flask(__name__)
    app.config.from_object(congigClass)

    db.init_app(app)
    loginManager.init_app(app)

    from files.routes.user import user
    app.register_blueprint(user)
    from files.routes.orders import orders
    app.register_blueprint(orders)

    with app.app_context():
        db.create_all()
    
    return app
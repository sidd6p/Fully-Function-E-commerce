from files import db, loginManager
from flask_login import UserMixin



@loginManager.user_loader
def loadUser(buyerId):
    return Buyer.query.get(int(buyerId))



class Buyer(db.Model, UserMixin):
    __bind_key__ = 'buyerdb'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pin = db.Column(db.Integer, nullable=False)

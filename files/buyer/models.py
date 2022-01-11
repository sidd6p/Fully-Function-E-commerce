from files import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(buyerId):
    return Buyer.query.get(int(buyerId))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # productId = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    # buyerId = db.Column(db.Integer, db.ForeignKey('Buyer.id'), nullable=False)

class WishList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # productId = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    # buyerId = db.Column(db.Integer, db.ForeignKey('Buyer.id'), nullable=False)

class Buyer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    # myWishlist = db.relationship('WishList', backref = 'buyer', lazy = True)
    # myCart = db.relationship('Cart', backref = 'buyer', lazy = True)
    # myHistory = db.relationship('History', backref = 'buyer', lazy = True)
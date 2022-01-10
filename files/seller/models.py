from files import db
from files.products.models import Products

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    shopName = db.Column(db.String(50), unique=True, nullable=False)
    shopLogo = db.Column(db.String(20), nullable=False, default='default.jpg')
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    prodIDs = db.relationship('Products', backref='seller', lazy=True)
    myHistory = db.relationship('History', backref = 'seller', lazy = True)

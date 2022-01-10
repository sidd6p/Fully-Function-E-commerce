from files import db
from datetime import datetime
from files.seller.models import Buyer
from files.seller.models import Seller

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productId =db.Column(db.Integer, db.ForeignKey('Buyer.id'), nullable=False)
    dateOfPurchase = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    buyerId = db.Column(db.Integer, db.ForeignKey('Buyer.id'), nullable=False)
    sellerId = db.Column(db.Integer, db.ForeignKey('Seller.id'), nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(50), nullable=False)
    productTitle = db.Column(db.String(100), nullable=False)
    productPhoto = db.Column(db.String(20), nullable=False, default='default.jpg')
    productDesc = db.Column(db.String(500), nullable=False)
    productPrice = db.Column(db.Integer(), nullable=False)
    sellerId = db.Column(db.Integer, db.ForeignKey('Seller.id'), nullable=False)

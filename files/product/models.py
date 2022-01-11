from files import db

class Products(db.Model):
    __bind_key__ = 'productdb'
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(50), nullable=False)
    productTitle = db.Column(db.String(100), nullable=False)
    productPhoto = db.Column(db.String(20), nullable=False, default='default.jpg')
    productDesc = db.Column(db.String(500), nullable=False)
    productPrice = db.Column(db.Integer(), nullable=False)
    # sellerId = db.Column(db.Integer, db.ForeignKey('Seller.id'), nullable=False)

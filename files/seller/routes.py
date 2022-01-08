from flask import Blueprint

seller = Blueprint('seller', __name__)

@seller.route("/seller-home")
def sellerHome():
    return "This is seller home"
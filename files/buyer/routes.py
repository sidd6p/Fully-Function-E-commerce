from flask import Blueprint

buyer = Blueprint('buyer', __name__)

@buyer.route("/buyer-home")
def buyerHome():
    return "This is buyer home"
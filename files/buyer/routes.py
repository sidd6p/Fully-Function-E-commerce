from flask import Blueprint

buyer = Blueprint('buyer', __name__)

@buyer.route("/buyer-home")
def home():
    return "This is buyer home"
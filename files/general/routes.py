from flask import Blueprint

general = Blueprint('general', __name__)

@general.route("/")
@general.route("/home")
def buyerHome():
    return "This is general home"
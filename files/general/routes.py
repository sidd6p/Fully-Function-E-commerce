from flask import Blueprint, render_template

general = Blueprint('general', __name__)

@general.route("/")
@general.route("/home")
def home():
    return render_template("general/home.html")
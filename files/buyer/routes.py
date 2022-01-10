from flask import Blueprint, flash, render_template, redirect, url_for
from files.buyer.forms import BuyerAccount 
from files.buyer.models import Buyer
from files import db

buyer = Blueprint('buyer', __name__)

@buyer.route("/buyer-home")
def home():
    return render_template('buyer/buyer-home.html',  title = "buyer Home", buyerHomePage = True, buyer = True)

@buyer.route("/create-buyer-home", methods = ["GET", "POST"])
def createBuyer():
    form = BuyerAccount()
    if form.validate_on_submit():
        newBuyer = Buyer(fname = form.buyerFirstName.data, lname = form.buyerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('buyer/create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True, buyer = True)

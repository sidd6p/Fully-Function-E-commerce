from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from files.buyer.forms import BuyerAccount
from files.buyer.models import Buyer
from files.general.models import Login
from files import db

buyer = Blueprint('buyer', __name__)

@buyer.route("/buyer-home")
def home():
    return render_template('buyer/buyer-home.html',  title = "buyer Home", buyerHomePage = True, buyer = True)

@buyer.route("/create-buyer", methods = ["GET", "POST"])
def register():
    form = BuyerAccount()
    if form.validate_on_submit():
        newBuyer = Buyer(fname = form.buyerFirstName.data, lname = form.buyerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('buyer/create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True, buyer = True)

@buyer.route("/buyer-login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('buyer.home'))
    form = Login()
    if form.validate_on_submit():
        hasBuyer = Buyer.query.filter_by(email = form.email.data).first()
        if hasBuyer and form.password.data == hasBuyer.password:
            login_user(hasBuyer)
            flash("Login Successfull", 'info')
            nextPage = request.args.get('next', 'buyer-home')
            return redirect(nextPage)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('general/login.html', form = form,  title = "Buyer-Login", loginPage = True, buyer = True)

@login_required
@buyer.route("/buyer-logout")
def logout():
    logout_user()
    return redirect(url_for('buyer.home'))
from flask import Blueprint, flash, render_template, redirect, url_for, request
from files.seller.forms import ShopAccount
from flask_login import login_required, current_user, logout_user, login_user
from files.general.models import Login
from files import db
from files.seller.models import Seller

seller = Blueprint('seller', __name__)

@seller.route("/seller-home")
def home():
    return render_template('seller/seller-home.html',  title = "Seller Home", sellerHomePage = True, seller = True)

@seller.route("/create-seller", methods = ["GET", "POST"])
def register():
    form = ShopAccount()
    if form.validate_on_submit():
        newBuyer = Seller(fname = form.sellerFirstName.data, lname = form.sellerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data, shopName= form.shopName.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("seller.home"))
    return render_template('seller/create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True, seller = True)


@seller.route("/seller-login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('seller.home'))
    form = Login()
    if form.validate_on_submit():
        hasBuyer = Seller.query.filter_by(email = form.email.data).first()
        if hasBuyer and form.password.data == hasBuyer.password:
            login_user(hasBuyer)
            flash("Login Successfully", 'info')
            nextPage = request.args.get('next', 'seller-home')
            return redirect(nextPage)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('general/login.html', form = form,  title = "Seller-Login", loginPage = True, seller = True)

@login_required
@seller.route("/seller-logout")
def logout():
    logout_user()
    return redirect(url_for('seller.home'))
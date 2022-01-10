from flask import Blueprint, flash, render_template, redirect, url_for
from files.seller.forms import ShopAccount
from files import db
from files.seller.models import Seller

seller = Blueprint('seller', __name__)

@seller.route("/seller-home")
def home():
    return render_template('seller/seller-home.html',  title = "Seller Home", sellerHomePage = True, seller = True)

@seller.route("/create-seller-home", methods = ["GET", "POST"])
def createShop():
    form = ShopAccount()
    if form.validate_on_submit():
        newBuyer = Seller(fname = form.sellerFirstName.data, lname = form.sellerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data, shopName= form.shopName.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("seller.home"))
    return render_template('seller/create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True, seller = True)
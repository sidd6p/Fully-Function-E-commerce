from flask import Blueprint, flash, render_template, redirect, url_for, request
from files.forms import ShopAccount, UploadProduct, Login
from flask_login import login_required, current_user, logout_user, login_user
from files import db
from files.models import Seller
import sqlite3

seller = Blueprint('seller', __name__)

@seller.route("/")
@seller.route("/seller-home")
def home():
    return render_template('seller-home.html',  title = "Seller Home", sellerHomePage = True, seller = True)

@seller.route("/create-seller", methods = ["GET", "POST"])
def register():
    form = ShopAccount()
    if form.validate_on_submit():
        newBuyer = Seller(fname = form.sellerFirstName.data, lname = form.sellerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data, shopName= form.shopName.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("seller.home"))
    return render_template('create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True, seller = True)


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
    return render_template('login.html', form = form,  title = "Seller-Login", loginPage = True, seller = True)

@seller.route("/seller-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('seller.home'))

@seller.route("/uploadProd", methods = ["GET", "POST"])
@login_required
def uploadProd():
    form = UploadProduct()
    if form.validate_on_submit():
        connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
        cursor = connection.cursor()
        query = "INSERT INTO products (productName, productType, productPhoto, productDesc, productPrice, shopName, sellerID, sellerAddress) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data =  (form.productName.data, form.productType.data, "default.jpg", form.productDesc.data, int(form.productPrice.data), current_user.shopName, int(current_user.id), current_user.address, )
        cursor.execute(query, data)
        connection.commit()
        connection.close()
        flash ("Product has been uploaded successfully", 'info')
        return redirect(url_for("seller.home"))
    return render_template('upload-product.html', form = form,  title = "Upload Product", uploadProdPage = True, seller = True)
    

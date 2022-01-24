from re import T
from this import d
from flask import Blueprint, flash, render_template, redirect, url_for, request
from files.forms import ShopAccount, UploadProduct, Login
from flask_login import login_required, current_user, logout_user, login_user
from files import db
from files.models import Seller
import sqlite3
from files.utils import dbquery, saveShopImage

seller = Blueprint('seller', __name__)

@seller.route("/")
@seller.route("/seller-home")
@login_required
def home():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products WHERE sellerID = (?)"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template('accounts.html',  prods = prods, title = "Seller-Account", accountPage = True)

@seller.route("/create-seller", methods = ["GET", "POST"])
def register():
    form = ShopAccount()
    if form.validate_on_submit():
        shopLogo = saveShopImage(form.shopLogo.data)
        newBuyer = Seller(fname = form.sellerFirstName.data, lname = form.sellerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data, shopName= form.shopName.data, shopLogo = shopLogo)
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

@seller.route("/upload-Products", methods = ["GET", "POST"])
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
    

@seller.route("/orders", methods = ["POST", "GET"])
@login_required
def order():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT  products.productName, products.productPhoto, orders.buyerName, orders.buyerEmail, orders.id, orders.status, orders.productID\
        FROM products INNER JOIN orders ON products.sellerID = orders.sellerID WHERE orders.sellerID = (?) AND orders.productID = products.id AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    orders = cursor.fetchall()
    if request.method == "POST":
        action = request.form.get("selleraction").split()
        query = " UPDATE orders SET status = ? WHERE id = ?"
        data = (str(action[0]), int(action[1]),)
        dbquery(query, data)
        flash("Order (Order Id: {}) has been {}".format(action[1], action[0]), 'info')
        return redirect(url_for("seller.order"))
    return render_template("orders.html", orders = orders, title = "Your Orders", orderPage = True)

@seller.route("/history")
@login_required
def history():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT products.productName, products.productPhoto, orders.buyerName, orders.buyerEmail, orders.id, orders.status, orders.productID\
         FROM products INNER JOIN orders ON orders.productID = products.id WHERE orders.sellerID = (?) AND (orders.status = 'Received' OR orders.status = 'Cancelled')"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    orders = cursor.fetchall()
    return render_template("orders.html", orders = orders, title = "Your History", historyPage = True)

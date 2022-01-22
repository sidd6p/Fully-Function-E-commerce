from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from files.forms import BuyerAccount, Login
from files.models import Buyer
from files import db
import sqlite3
from files.utils import dbquery

buyer = Blueprint('buyer', __name__)

@buyer.route("/")
@buyer.route("/buyer-home")
@buyer.route("/buy")
def home():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Prodcts", allProdsPage = True)

@buyer.route("/create-buyer", methods = ["GET", "POST"])
def register():
    form = BuyerAccount()
    if form.validate_on_submit():
        newBuyer = Buyer(fname = form.buyerFirstName.data, lname = form.buyerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True)

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
    return render_template('login.html', form = form,  title = "Buyer-Login", loginPage = True)


@buyer.route("/buyer-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('buyer.home'))

@buyer.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('accounts.html',  title = "Buyer-Account", accountPage = True)


@buyer.route("/wishlist-page")
@login_required
def wishlist():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN basket ON basket.productID = products.id WHERE basket.buyerID = (?) AND basket.btype = 'w'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Wishlist", bType = "wishlist")

@buyer.route("/cart-page")
@login_required
def cart():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN basket ON basket.productID = products.id WHERE basket.buyerID = (?) AND basket.bType = 'c'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Cart", bType = "cart")

@buyer.route("/order-page")
@login_required
def order():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN orders ON orders.productID = products.id WHERE orders.buyerID = (?) AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Your Orders", bType = "order", status = "Accepted")


@buyer.route("/buyer-action", methods = ["POST", "GET"])
@login_required
def buyerAction():
    if request.method == "POST":
        action = request.form.get("buyeraction").split()
        if action[0] == "0":
            query = "UPDATE orders SET status = ? WHERE id = ?"
            data = (str(action[1]), int(action[2]), ) 
            dbquery(query, data)
            flash("Your order (Order Id: {}) has been {}".format(int(action[2]), str(action[1])), 'info') 
        if action[0] == "1":
            query = "INSERT INTO orders (productID, buyerID, sellerID, buyerName, buyerEmail) VALUES (?, ?, ?, ?, ?)"
            data = (int(action[1]), int(current_user.id), int(action[2]), current_user.fname, current_user.email, ) 
            dbquery(query, data)
            flash("Your order has been placed", 'info')
        if action[0] == "2":
            query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
            data = (int(action[1]), int(current_user.id), "c", ) 
            dbquery(query, data)
            flash("Item has been added to your cart", 'info')
        if action[0] == "3":
            query = """ INSERT OR REPLACE into basket VALUES (?, ?, ?)"""
            data = (int(action[1]), int(current_user.id), "w", ) 
            dbquery(query, data)
            flash("Item has been added to your wishlist", 'info')    
        if action[0] == "-2":
            query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
            data = (int(action[1]), int(current_user.id), ) 
            dbquery(query, data)
            flash("Item has been removed from your cart", 'info')    
        if action[0] == "-3":
            query = "DELETE FROM basket WHERE productID = ? AND buyerID = ?"
            data = (int(action[1]), int(current_user.id), ) 
            dbquery(query, data)
            flash("Item has been removed from your wishlist", 'info')   
    return redirect(url_for('buyer.order'))

@buyer.route("/your-history")
@login_required
def history():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN orders ON orders.productID = products.id WHERE orders.buyerID = (?) AND (orders.status = 'Received' OR orders.status = 'Cancelled')"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Your History", bType = "order", status = "Accepted")

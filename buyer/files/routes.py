from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from files.forms import BuyerAccount, Login
from files.models import Buyer
from files import db
import sqlite3

buyer = Blueprint('buyer', __name__)

@buyer.route("/")
@buyer.route("/buyer-home")
def home():
    return render_template('buyer-home.html',  title = "buyer Home", buyerHomePage = True, buyer = True)

@buyer.route("/create-buyer", methods = ["GET", "POST"])
def register():
    form = BuyerAccount()
    if form.validate_on_submit():
        newBuyer = Buyer(fname = form.buyerFirstName.data, lname = form.buyerLastName.data, email = form.email.data, password = form.pswd.data, address = form.address.data, city = form.city.data, state = form.state.data, pin = form.pin.data)
        db.session.add(newBuyer)
        db.session.commit()
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True, buyer = True)

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
    return render_template('login.html', form = form,  title = "Buyer-Login", loginPage = True, buyer = True)


@buyer.route("/buyer-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('buyer.home'))

@buyer.route("/buy")
@login_required
def prodPages():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Prodcts", allProdsPage = True, buyer = True)

@buyer.route("/buyer-action", methods = ["POST"])
@login_required
def buyerAction():
    if request.method == "POST":
        action = request.form.get("buyeraction").split()
        if action[0] == "1":
            connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\history.db')
            cursor = connection.cursor()
            query = "INSERT INTO histories (productID, buyerID, sellerID) VALUES (?, ?, ?)"
            data = (int(action[1]), int(current_user.id), int(action[2])) 
            cursor.execute(query, data)  
            connection.commit()
            connection.close()
        if action[0] == "2":
            connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\buyer\files\databases\cart.db')
            cursor = connection.cursor()
            query = "INSERT INTO carts (productID, buyerID) VALUES (?, ?)"
            data = (int(action[1]), int(current_user.id)) 
            cursor.execute(query, data)  
            connection.commit()
            connection.close()
        if action[0] == "3":
            connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\buyer\files\databases\wishlist.db')
            cursor = connection.cursor()
            query = "INSERT INTO wishlists (productID, buyerID) VALUES (?, ?)"
            data = (int(action[1]), int(current_user.id)) 
            cursor.execute(query, data)  
            connection.commit()
            connection.close()       
        if action[0] == "4":
            return redirect(url_for('buyer.buyerEnquiry'))          
    return "OK"

@buyer.route("/buyer-enquiry")
@login_required
def buyerEnquiry():
    return "Enquiry Done"
from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from files.forms import ShopAccount, Login
from flask_login import login_required, current_user, logout_user, login_user
from files import db
from files.models import Seller
import sqlite3
from files.utils import saveShopImage, add_seller


user = Blueprint('user', __name__)

@user.route("/")
@user.route("/seller-home")
@login_required
def home():
    connection = sqlite3.connect(r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db')
    cursor = connection.cursor()
    query = "SELECT * FROM products WHERE sellerID = (?)"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template('accounts.html',  prods = prods, title = "Seller-Account", accountPage = True, prodDirPath = "C:\\Users\\siddpc\\OneDrive\\Desktop\\Projects\\offline-e-commerce\\databases\\images\\products\\"
)

@user.route("/create-seller", methods = ["GET", "POST"])
def register():
    form = ShopAccount()
    if form.validate_on_submit():
        add_seller(form)
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("user.home"))
    return render_template('create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True, seller = True)


@user.route("/seller-login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
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

@user.route("/seller-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.home'))
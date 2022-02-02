from files import utils
from flask import Blueprint, flash, render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from files.forms import BuyerAccount, Login
from files.models import Buyer
from files.config import DB_ADDRESS
import sqlite3


user = Blueprint('user', __name__)


@user.route("/")
@user.route("/buyer-home")
@user.route("/buy")
def home():
    connection = sqlite3.connect(DB_ADDRESS)
    cursor = connection.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Prodcts", allProdsPage = True)


@user.route("/create-buyer", methods = ["GET", "POST"])
def register():
    form = BuyerAccount()
    if form.validate_on_submit():
        utils.add_buyer(form_data=form)
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True)

@user.route("/buyer-login", methods = ["POST", "GET"])
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


@user.route("/buyer-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('buyer.home'))


@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('accounts.html',  title = "Buyer-Account", accountPage = True)

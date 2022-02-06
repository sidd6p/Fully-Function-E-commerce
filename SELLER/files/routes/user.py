from files.models import Seller

from flask import   (
                    Blueprint, 
                    flash, 
                    render_template, 
                    redirect, 
                    url_for, 
                    request
                    )

from files.forms import (
                        ShopAccount, 
                        Login
                        )

from flask_login import (
                        login_required,
                        current_user, 
                        logout_user, 
                        login_user
                        )

from files.utils import (
                        add_seller, 
                        get_products_details,
                        get_this_product,
                        verify_pswd
                        )



user = Blueprint('user', __name__)



################ HOME_ROUTE ################
@user.route("/", methods=["POST", "GET"])
@user.route("/seller-home", methods=["POST", "GET"])
@login_required
def home():
    if request.method == "GET":
        search = "Your Products"
        prods = get_products_details(current_user.id)
    else:
        this_product = request.form['productNeed']
        search = this_product
        prods = get_this_product(current_user.id, this_product.strip())
    return render_template('accounts.html',  prods = prods, title = "Seller-Account", search = search or "Your Products", accountPage = True)


################ REGISRTATION-ROUTE ################
@user.route("/create-seller", methods = ["GET", "POST"])
def register():
    form = ShopAccount()
    if form.validate_on_submit():
        add_seller(form)
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("user.home"))
    return render_template('create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True, seller = True)


################ LOGIN-ROUTE ################
@user.route("/seller-login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = Login()
    if form.validate_on_submit():
        hasBuyer = Seller.query.filter_by(email = form.email.data).first()
        if hasBuyer and verify_pswd(form.password.data, hasBuyer.password):
            login_user(hasBuyer)
            flash("Login Successfully", 'info')
            nextPage = request.args.get('next', 'seller-home')
            return redirect(nextPage)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form = form,  title = "Seller-Login", loginPage = True, seller = True)


################ LOGOUT-ROUTE ################
@user.route("/seller-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.home'))
from files import utils

from files.models import Buyer

from flask import   (
                    Blueprint,
                    flash,
                    render_template,
                    redirect,
                    url_for,
                    request,
                    Blueprint
                    )

from flask_login import     (
                            login_required,
                            current_user, 
                            login_user, 
                            logout_user
                            )

from files.forms import     (
                            BuyerAccount, 
                            Login
                            )



user = Blueprint('user', __name__)



#################### HOME-ROUTE #################### 
@user.route("/")
@user.route("/buyer-home")
@user.route("/buy")
def home():
    prods = utils.get_products_details()
    return render_template("show-products.html", prods = prods, title = "Products", allProdsPage = True)


#################### SERACH-PRODUCT-ROUTE #################### 
@user.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "POST":            
        this_product = request.form['productNeed']
        prods = utils.get_this_product(this_product.strip())
    else:
        return redirect(url_for('user.home'))
    return render_template("show-products.html", prods = prods, title = this_product or "Products", allProdsPage = True)


#################### REGISTRATION-ROUTE ####################
@user.route("/create-buyer", methods = ["GET", "POST"])
def register():
    form = BuyerAccount()
    if form.validate_on_submit():
        utils.add_buyer(form_data=form)
        flash("Your buyer home has been created successfully", 'info')
        return redirect(url_for("buyer.home"))
    return render_template('create-buyer.html', form = form,  title = "Create Your Buyer Account", createBuyerPage = True)


#################### LOGIN-ROUTE ####################
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


#################### LOGOUT-ROUTE ####################
@user.route("/buyer-logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.home'))


#################### ACCOUNT-ROUTE ####################
@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('accounts.html',  title = "Buyer-Account", accountPage = True)

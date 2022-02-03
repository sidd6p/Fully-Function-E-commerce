from files.forms import UploadProduct

from flask_login import login_required

from flask import   (
                    Blueprint,  
                    flash, 
                    render_template, 
                    redirect, 
                    url_for, 
                    request, 
                    Blueprint
                    )


from files.utils import     (
                            add_product,
                            update_order_status, 
                            get_all_orders,
                            get_orders_history
                            )



products = Blueprint('products', __name__)



################ UPLOAD-PRODUCT-ROUTE ################
@products.route("/upload-Products", methods = ["GET", "POST"])
@login_required
def uploadProd():
    form = UploadProduct()
    if form.validate_on_submit():
        add_product(form)
        flash ("Product has been uploaded successfully", 'info')
        return redirect(url_for("user.home"))
    return render_template('upload-product.html', form = form,  title = "Upload Product", uploadProdPage = True, seller = True)
    

################ ORDERS-ROUTE ################
@products.route("/orders", methods = ["POST", "GET"])
@login_required
def order():
    orders = get_all_orders()
    if request.method == "POST":
        action = request.form.get("selleraction").split()
        update_order_status(action)
        flash("Order (Order Id: {}) has been {}".format(action[1], action[0]), 'info')
        return redirect(url_for("products.order"))
    return render_template("orders.html", orders = orders, title = "Your Orders", orderPage = True)


################ HISTORY-ROUTE ################
@products.route("/history")
@login_required
def history():
    orders = get_orders_history()
    return render_template("orders.html", orders = orders, title = "Your History", historyPage = True)

from flask import   (
                    Blueprint,
                    flash,
                    render_template,
                    redirect,
                    url_for, 
                    request, 
                    Blueprint
                    )

from flask_login import (
                        login_required,
                        )  

from files.utils import (
                        get_wish_details,
                        get_cart_details,
                        get_order_details,
                        get_history_details,
                        update_status,
                        place_order,
                        add_to_cart,
                        delete_from_cart,
                        add_to_wishlist,
                        delete_from_wishlist
                        )



orders = Blueprint('orders', __name__)



#################### WHISHLIST-ROUTE #################### 
@orders.route("/wishlist-page")
@login_required
def wishlist():
    prods = get_wish_details()
    return render_template("show-products.html", prods = prods, title = "Wishlist", bType = "wishlist")


#################### CART-ROUTE #################### 
@orders.route("/cart-page")
@login_required
def cart():
    prods = get_cart_details()
    return render_template("show-products.html", prods = prods, title = "Cart", bType = "cart")


#################### ORDER-ROUTE #################### 
@orders.route("/order-page")
@login_required
def order():
    prods = get_order_details()
    return render_template("show-products.html", prods = prods, title = "Your Orders", bType = "order", status = "Accepted")


#################### BUYING-RELATED-ROUTE #################### 
@orders.route("/buyer-action", methods = ["POST", "GET"])
@login_required
def buyerAction():
    if request.method == "POST":
        action = request.form.get("buyeraction").split()
        if action[0] == "0":
            update_status(action)
            flash("Your order (Order Id: {}) has been {}".format(int(action[2]), str(action[1])), 'info') 
        if action[0] == "1":
            place_order(action)
            flash("Your order has been placed", 'info')
        if action[0] == "2":
            add_to_cart(action)
            flash("Item has been added to your cart", 'info')
        if action[0] == "3":
            add_to_wishlist(action)
            flash("Item has been added to your wishlist", 'info')    
        if action[0] == "-2":
            delete_from_cart(action)
            flash("Item has been removed from your cart", 'info')    
        if action[0] == "-3":
            delete_from_wishlist(action)
            flash("Item has been removed from your wishlist", 'info')   
    return redirect(url_for('user.home'))



#################### HISTORY #################### 
@orders.route("/your-history")
@login_required
def history():
    prods = get_history_details()
    return render_template("show-products.html", prods = prods, title = "Your History", bType = "order", status = "Accepted")

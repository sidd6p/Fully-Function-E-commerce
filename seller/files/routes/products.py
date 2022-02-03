from flask import Blueprint, flash, render_template, redirect, url_for, request, Blueprint
from files.forms import UploadProduct
from flask_login import login_required, current_user
import sqlite3
from files.utils import dbquery, add_product


products = Blueprint('products', __name__)

@products.route("/upload-Products", methods = ["GET", "POST"])
@login_required
def uploadProd():
    form = UploadProduct()
    if form.validate_on_submit():
        add_product(form)
        flash ("Product has been uploaded successfully", 'info')
        return redirect(url_for("user.home"))
    return render_template('upload-product.html', form = form,  title = "Upload Product", uploadProdPage = True, seller = True)
    

@products.route("/orders", methods = ["POST", "GET"])
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
        return redirect(url_for("products.order"))
    return render_template("orders.html", orders = orders, title = "Your Orders", orderPage = True)

@products.route("/history")
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

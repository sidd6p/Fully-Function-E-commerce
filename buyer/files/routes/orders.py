from files import utils
from flask import Blueprint, flash, render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
import sqlite3
from files.utils import dbquery
from files.config import DB_ADDRESS

orders = Blueprint('orders', __name__)

@orders.route("/wishlist-page")
@login_required
def wishlist():
    connection = sqlite3.connect(DB_ADDRESS)
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN basket ON basket.productID = products.id WHERE basket.buyerID = (?) AND basket.btype = 'w'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Wishlist", bType = "wishlist")

@orders.route("/cart-page")
@login_required
def cart():
    connection = sqlite3.connect(DB_ADDRESS)
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN basket ON basket.productID = products.id WHERE basket.buyerID = (?) AND basket.bType = 'c'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Cart", bType = "cart")

@orders.route("/order-page")
@login_required
def order():
    connection = sqlite3.connect(DB_ADDRESS)
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN orders ON orders.productID = products.id WHERE orders.buyerID = (?) AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Your Orders", bType = "order", status = "Accepted")


@orders.route("/buyer-action", methods = ["POST", "GET"])
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
    return redirect(url_for('user.home'))

@orders.route("/your-history")
@login_required
def history():
    connection = sqlite3.connect(DB_ADDRESS)
    cursor = connection.cursor()
    query = "SELECT * FROM products INNER JOIN orders ON orders.productID = products.id WHERE orders.buyerID = (?) AND (orders.status = 'Received' OR orders.status = 'Cancelled')"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    prods = cursor.fetchall()
    return render_template("show-products.html", prods = prods, title = "Your History", bType = "order", status = "Accepted")

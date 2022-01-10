from flask import Blueprint, render_template
product = Blueprint('product', __name__)

@product.route("/buy")
def allProds():
    allProds = {"image" : "static\img\download.jpg", "seller": "Siddhartha", "price" :1000, "address": "Kanpur UP, 285123" }
    prods = [allProds, allProds,allProds, allProds, allProds]
    return render_template("products/show-prods.html", prods = prods, title = "Prodcts", allProdsPage = True, buyer = True)

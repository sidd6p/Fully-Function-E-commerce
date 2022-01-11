from flask import Blueprint, render_template, flash, redirect, url_for
from files.product.forms import UploadProduct
from files.product.models import Products
from flask_login import login_required
from files import db

product = Blueprint('product', __name__)

@login_required
@product.route("/buy")
def allProds():
    allProds = {"image" : "default.jpg", "seller": "Siddhartha", "price" :1000, "address": "Kanpur UP, 285123" }
    prods = [allProds, allProds,allProds, allProds, allProds]
    return render_template("products/show-prods.html", prods = prods, title = "Prodcts", allProdsPage = True, buyer = True)

@login_required
@product.route("/uploadProd", methods = ["GET", "POST"])
def uploadProd():
    form = UploadProduct()
    if form.validate_on_submit():
        newProducts = Products(productName = form.productName.data, productTitle = form.productTitle.data, productDesc = form.productDesc.data, productPrice = form.productPrice.data)
        db.session.add(newProducts)
        db.session.commit()
        flash ("Product has been uploaded successfully", 'info')
        return redirect(url_for("seller.home"))
    return render_template('products/upload-product.html', form = form,  title = "Upload Product", uploadProdPage = True, seller = True)
    

from flask import Blueprint, flash, render_template, redirect, url_for
from files.seller.forms import UploadProduct, ShopAccount

seller = Blueprint('seller', __name__)

@seller.route("/seller-home")
def sellerHome():
    return render_template('seller/home.html',  title = "Seller Home", sellerHomePage = True)

@seller.route("/create-seller-home", methods = ["GET", "POST"])
def createShop():
    form = ShopAccount()
    if form.validate_on_submit():
        flash("Your seller home has been created successfully", 'info')
        return redirect(url_for("seller.sellerHome"))
    return render_template('seller/create-shop.html', form = form,  title = "Create Your Shop", createShopPage = True)

@seller.route("/uploadProd", methods = ["GET", "POST"])
def uploadProd():
    form = UploadProduct()
    if form.validate_on_submit():
        flash ("Product has been uploaded successfully", 'info')
        return redirect(url_for("seller.sellerHome"))
    return render_template('seller/upload-product.html', form = form,  title = "Upload Product", uploadProdPage = True)
    

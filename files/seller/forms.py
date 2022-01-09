from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, TextAreaField, PasswordField, EmailField
from wtforms.validators import Length, DataRequired, Email, EqualTo, NumberRange

class UploadProduct(FlaskForm):
    productName = StringField("Product Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Product Name length should be between 5 to 50 characters")])
    productTitle = StringField("Product Title", validators = [DataRequired(), Length(min = 5, max = 100, message = "Product Name length should be between 5 to 100 characters")])
    productDesc = TextAreaField("Product Description", validators = [DataRequired(), Length(min = 5, max = 500, message = "Product Name length should be between 5 to 500 characters")])
    productPrice = IntegerField("Product Price", validators = [DataRequired()])
    authentication = BooleanField("All details provide by you are correct and authenticated properly by you", validators = [DataRequired()])
    submit = SubmitField("Upload Product")


class ShopAccount(FlaskForm):
    sellerFirstName = StringField("First Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characters")])
    sellerLastName = StringField("Last Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characters")])
    email = StringField("Email", validators = [DataRequired(message = "This field is required"), Email(message = "Provide a valid Email-Id")])
    pswd = PasswordField("Password", validators = [DataRequired(message = "This field is required"), Length(min = 8, message = "Minimum Length should be 8")])
    confirmPswd = PasswordField("Confirm Password", validators = [DataRequired(message = "This field is required"), EqualTo('pswd', message = "Password did not match!")])
    shopName = StringField("Title of your shop", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characte")])
    ZipPinCode = IntegerField("PIN or ZIP code of your physical shop", validators = [DataRequired(), NumberRange(min = 000000, max = 999999)])
    authentication = BooleanField("All details provide by you are correct and authenticated properly by you", validators = [DataRequired()])
    submit = SubmitField("Create Shop")
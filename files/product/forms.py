from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, IntegerField, TextAreaField, PasswordField, EmailField
from wtforms.validators import Length, DataRequired, Email, EqualTo, NumberRange

class UploadProduct(FlaskForm):
    productName = StringField("Product Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Product Name length should be between 5 to 50 characters")])
    productTitle = StringField("Product Title", validators = [DataRequired(), Length(min = 5, max = 100, message = "Product Name length should be between 5 to 100 characters")])
    productPhoto = FileField("Shop Logo/Picture", validators = [DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'png'], message = "Allowed file type are: 'jpg', 'png', 'jpeg', 'png'")])
    productDesc = TextAreaField("Product Description", validators = [DataRequired(), Length(min = 5, max = 500, message = "Product Name length should be between 5 to 500 characters")])
    productPrice = IntegerField("Product Price", validators = [DataRequired()])
    submit = SubmitField("Upload Product")

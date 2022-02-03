from flask_wtf import FlaskForm

from files.models import Buyer

from wtforms import     (
                        StringField, 
                        SubmitField, 
                        IntegerField, 
                        TextAreaField, 
                        PasswordField, 
                        EmailField, 
                        BooleanField
                        )

from wtforms.validators import  (
                                Length, 
                                DataRequired, 
                                Email, 
                                EqualTo, 
                                NumberRange, 
                                ValidationError
                                )




class BuyerAccount(FlaskForm):
    buyerFirstName = StringField("First Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characters")])
    buyerLastName = StringField("Last Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characters")])
    email = EmailField("Email", validators = [DataRequired(message = "This field is required"), Email(message = "Provide a valid Email-Id")])
    pswd = PasswordField("Password", validators = [DataRequired(message = "This field is required"), Length(min = 8, message = "Minimum Length should be 8")])
    confirmPswd = PasswordField("Confirm Password", validators = [DataRequired(message = "This field is required"), EqualTo('pswd', message = "Password did not match!")])
    address = TextAreaField("Address/Locality", validators = [DataRequired(), Length(min = 5, max = 500, message = "Field length shoud be bewteen  5 to 500 characte")])
    city = StringField("City", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characte")])
    state = StringField("State", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characte")])
    pin = IntegerField("PIN", validators = [DataRequired(), NumberRange(min = 000000, max = 999999)])
    submit = SubmitField("Create Shop")

    def validate_email(self, email):
        hasBuyer = Buyer.query.filter_by(email=email.data).first()
        if hasBuyer:
            raise ValidationError('That email is taken. Please choose a different one.')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
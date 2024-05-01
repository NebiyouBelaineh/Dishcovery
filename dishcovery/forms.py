from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from dishcovery.models import User
from dishcovery.models import db_storage

class RegisterForm(FlaskForm):
    """
    Class that deal with registration form
    """
    def validate_email_address(self, email_to_check):
        user = db_storage.getSession().query(User).filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email address already exists! Please try different email address")
    
    first_name = StringField(label="First name", validators=[DataRequired()])
    last_name = StringField(label="Last name", validators=[DataRequired()])
    email_address = StringField(label="Email address", validators=[Email(message="Email is not valid"), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6, message="Password minimum length is 6 characters"), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo('password1', message="Password and confirmation password doesn't match"),DataRequired()])
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    """
    class that deals with login forms
    """
    email_address = StringField(label="Email address", validators=[Email(message="Email is not valid"), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6, message="Password minimum length is 6 characters"), DataRequired()])
    submit = SubmitField(label="Sign in")

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import InputRequired, Optional, Email


class UserForm(FlaskForm):


    username = StringField("Username",
                       validators=[InputRequired()])
    password = PasswordField("Password",
                        validators=[InputRequired(), ])
    email = EmailField("Email Address",
                        validators=[InputRequired()])
    first_name = StringField("First Name",
                       validators=[InputRequired()])
    last_name = StringField("Last Name",
                       validators=[InputRequired()])
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    rem_me = BooleanField("Remember Password")
    submit = SubmitField("Sign In")

class RegiterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up")
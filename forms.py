from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email
class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Username can't be blank")])
    email = StringField("Email", validators=[InputRequired(message="Username can't be blank"), Email(message="Invalid Email")])
    first_name = StringField("First Name", validators=[InputRequired(message="Username can't be blank")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Username can't be blank")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
    
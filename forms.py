from flask_wtf import FlaskForm
#passwordFifeld gives you the dots when you are typring
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class Registration(FlaskForm):
    username=StringField("Username", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])
    email=StringField("E-mail", validators=[InputRequired()])
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()]) 

class Login(FlaskForm):
    username=StringField("Username", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired()])
    content=StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """don't do anything"""







    
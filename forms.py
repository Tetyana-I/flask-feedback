from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class UserRegisterForm(FlaskForm):
    """ Form for registering a new user """
    username = StringField("User Name",  validators=[InputRequired(message="Please enter your username"), 
                                        Length(max=20, message="You cannot use more than 20 characters for your username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter your password")])  
    email = StringField("Email", validators=[InputRequired(message="Please enter your email")])
    first_name = StringField("First Name", [Length(max=30, message="You cannot use more than 30 characters for your first name"),
                                                     InputRequired(message="Please enter your first name")])
    last_name = StringField("Last Name", validators=[Length(max=30, message="You cannot use more than 30 characters for your last name"),
                                                     InputRequired(message="Please enter your last name")])


class UserLoginForm(FlaskForm):
    """ Form for user login """
    username = StringField("User Name",  validators=[InputRequired(message="Please enter your username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter your password")])  
    

class FeedbackForm(FlaskForm):
    """ Form to create a feedback """
    title = StringField("Title", validators=[Length(max=100, message="Title cannot be more than 100 characters"),
                                                    InputRequired(message="Please enter a title")])
    content = TextAreaField("Content",  validators=[InputRequired(message="Please enter your feedback")])
    
    
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length, Email, EqualTo


class SignUp(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    Email = StringField('Email',validators=[DataRequired(),Email()])
    Password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),
                                                                  EqualTo('password')])
    submit = SubmitField('SignUp')

class Login(FlaskForm):

    Email = StringField('Email',validators=[DataRequired(),Email()])
    Password=PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminSignUp(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    Email = StringField('Email',validators=[DataRequired(),Email()])
    Password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),
                                                                  EqualTo('password')])
    Railway_ID = IntegerField('Railway ID',validators=[DataRequired(),Length(min=5,max=20)])
    submit = SubmitField('AdminSignUp')

class AdminLogin(FlaskForm):

    Email = StringField('Email',validators=[DataRequired(),Email()])
    Password=PasswordField('Password',validators=[DataRequired()])
    Railway_ID = IntegerField('Railway ID',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
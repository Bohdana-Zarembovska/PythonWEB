from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp
from app.models import User
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired("Email is required"), Email()])
    password = PasswordField(label='Password', validators=[DataRequired("Password is required")])
    remember = BooleanField(label="Remember me")
    submit = SubmitField(label="Sign in")

class RegistrationForm(FlaskForm):
    username = StringField(label='User name', validators=[
            DataRequired("Name is required"),
            Length(min=4, max=14, message="Min length - 4, max - 14 symbols"),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0, 'Username must have only lettters, numbers, dots or underscores')
        ])
    email = StringField(label='Email', validators=[DataRequired("Email is required"), Email()])
    password = PasswordField(label='Password', validators=[
            DataRequired("Password is required"), 
            Length(min=7, message="Min length - 7 symbols")
        ])
    confirm_password = PasswordField(label='Confirm password', validators=[DataRequired("Confirm password is required"),EqualTo('password')])
    submit = SubmitField(label="Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(" ", validators=[
        DataRequired("Це поле обов'язкове"),
    ])
    new_password = PasswordField(" ", validators=[
        DataRequired("Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль повинен бути від 4 до 10 символів"),
    ])
    confirm_password = PasswordField(" ", validators=[
        DataRequired("Це поле обов'язкове"),
        EqualTo('new_password', message='Паролі повинні співпадати')
    ])
    submit = SubmitField("Change")

class CreateTodo(FlaskForm):
    new_task = StringField(" ", validators=[DataRequired("You should writesomething here"), Length(min=1, max=100)])
    description = StringField(" ", validators=[DataRequired("You should writesomething here too"), Length(min=1, max=200)])
    submit = SubmitField("Create")
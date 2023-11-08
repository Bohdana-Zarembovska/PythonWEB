from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
class LoginForm(FlaskForm):
    username = StringField("", validators=[DataRequired("Це поле обовʼязкове")])
    password = PasswordField("", validators=[
                            DataRequired("Тут повинно бути від 4 до 10 символів"),
                            Length(min=4, max=10)
                        ])
    remember = BooleanField("Запамʼятати")
    submit = SubmitField("Увійти")

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
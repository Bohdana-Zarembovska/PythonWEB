from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired("Title is required")])
    due_date = DateField(label='Due date')
    submit = SubmitField(label="Save")

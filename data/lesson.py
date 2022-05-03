from flask_wtf import FlaskForm
from wtforms import StringField


class LoginForm(FlaskForm):
    lesson = StringField('Название урока')
    day = StringField('DD.MM.YYYY HH:MM')
    submit = SubmitField('Записаться')

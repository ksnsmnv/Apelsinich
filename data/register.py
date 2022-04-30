from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('ФИО')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', [DataRequired(),
                                        EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')
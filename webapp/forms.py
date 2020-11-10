from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SendForm(FlaskForm):
    """Форма отправки email"""

    email = StringField('Email:', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class LoginForm(FlaskForm):

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить меня', render_kw={"class": 'form-check-input'})
    submit = SubmitField('Отправить', default=True, render_kw={"class": "btn btn-primary"})


class AssignForm(FlaskForm):

    selection = SelectField(u'Executor', coerce=int)

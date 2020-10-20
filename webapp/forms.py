from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class SendForm(FlaskForm):
    """Форма отправки email"""

    email = StringField('Email:', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class LoginForm(FlaskForm):
    """Форма авторизации"""

    login = StringField('login', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-primary'})

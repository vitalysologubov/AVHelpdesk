from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Форма авторизации"""

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', render_kw={"class": 'form-check-input'})


class TicketsForm(FlaskForm):
    """Список заявок"""

    submit_login = SubmitField('Войти', render_kw={'class': 'btn btn-primary navbar-btn'})
    submit_logout = SubmitField('Выйти', render_kw={'class': 'btn btn-danger navbar-btn'})


class TicketForm(FlaskForm):
    """Форма заявки"""

    client_name = StringField('Клиент:', render_kw={'readonly class': 'form-control'})
    staff_name = StringField('Сотрудник:', render_kw={'readonly class': 'form-control'})
    created_date = StringField('Дата:', render_kw={'readonly class': 'form-control'})
    urgency = StringField('Срочность:', render_kw={'readonly class': 'form-control'})
    subject = StringField('Тема:', render_kw={'readonly class': 'form-control'})
    reply = TextAreaField('Ответ:', render_kw={'class': 'form-control', "rows": "10", "style": "resize: none;"})
    submit_logout = SubmitField('Выйти', render_kw={'class': 'btn btn-danger navbar-btn'})
    submit_send = SubmitField('Отправить ответ', render_kw={'class': 'btn btn-primary btn-block'})
    submit_close = SubmitField('Закрыть заявку', render_kw={'class': 'btn btn-success btn-block'})
    submit_assign = SubmitField('Назначить', render_kw={'class': 'btn btn-warning btn-block'})
    selection = SelectField(u'Executor', coerce=int)


class SendForm(FlaskForm):
    """Форма отправки email"""

    email = StringField('Email:', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})

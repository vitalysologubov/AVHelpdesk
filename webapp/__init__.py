from flask import flash, Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.forms import SendForm
from webapp.models import db
from webapp.send_email import send_email


def create_app():
    """Создание приложения"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        """Главная страница: обработка входящих писем"""

        messages = fetch_mail()
        add_ticket(messages)

        return 'Работаем!'

    @app.route('/send')
    def email_form():
        """Форма отправки email"""

        form = SendForm()
        return render_template('email_form.html', title='Отправка email', form=form)

    @app.route('/email_proccess', methods=['POST'])
    def email_proccess():
        """Процесс отправки email"""

        form = SendForm()
        subject = 'Тестовая тема'
        message = 'Тестовое сообщение'

        if form.validate_on_submit():
            receiver = form.email.data
            message = send_email(receiver, subject, message)
            flash(message)

            return redirect(url_for('email_form'))

    return app

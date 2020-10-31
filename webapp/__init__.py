from flask import flash, Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from sqlalchemy import and_
from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.forms import SendForm
from webapp.models import db, Ticket, TicketStatus, TicketUrgency
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

    @app.route('/tickets')
    def tickets():
        """Список всех заявок"""

        tickets = db.session.query(
            Ticket.id,
            Ticket.created_date,
            Ticket.subject,
            TicketUrgency.urgency,
            TicketStatus.status
        ).filter(and_(
            Ticket.id_urgency == TicketUrgency.id,
            Ticket.id_status == TicketStatus.id)
        ).all()

        return render_template('tickets.html', title="Заявки", tickets=tickets)

    return app

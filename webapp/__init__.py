import re
from flask import flash, Flask, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate
from sqlalchemy import and_

from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.models import db, Staff, Ticket, TicketStatus, TicketUrgency
from webapp.forms import AssignForm, LoginForm, SendForm, TicketForm, TicketsForm
from webapp.send_email import send_email
from webapp.models import db, Client, Message, Staff, Ticket, TicketStatus, TicketUrgency, CLOSED


def create_app():
    """Создание приложения"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        """Получение ИД пользователя"""

        return Staff.query.get(user_id)

    @app.route('/login')
    def login():
        """Авторизация"""

        if current_user.is_authenticated:
            return redirect(url_for('index'))

        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login_form.html', title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        """Процесс авторизации"""

        form = LoginForm()

        if form.validate_on_submit():
            user = Staff.query.filter_by(username=form.username.data).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))

            flash('Неправильный логин или пароль!')
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        """Выход из системы"""

        logout_user()
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        """
        Список всех заявок.
        Если авторизован сотрудник с ролью "Администратор", то загружается список заявок, которые ещё не назначены на
        других сотрудников. Сотрудник с такой ролью может может назначить заявку на другого.
        Если авторизован сотрудник с ролью "Сотрудник", то загружается список заявок, назначенных только на этого
        сотрудника.
        """

        tickets_form = TicketsForm()

        if current_user.is_authenticated:
            if current_user.is_admin:
                tickets = db.session.query(
                    Ticket.id, Ticket.created_date, Ticket.subject, TicketUrgency.urgency, TicketStatus.status,
                    Staff.name
                    ).outerjoin(
                        Staff, Staff.id == Ticket.id_staff
                    ).join(
                        TicketUrgency, TicketUrgency.id == Ticket.id_urgency
                    ).join(
                        TicketStatus, TicketStatus.id == Ticket.id_status
                    ).all()
            else:
                tickets = db.session.query(
                    Ticket.id, Ticket.created_date, Ticket.subject, TicketUrgency.urgency, TicketStatus.status,
                    Staff.name
                    ).filter(
                        Ticket.id_staff == current_user.id,
                        Ticket.id_urgency == TicketUrgency.id,
                        Ticket.id_status == TicketStatus.id,
                        Staff.id == current_user.id
                    ).all()

            return render_template(
                'tickets_form.html', title="AVHelpdesk", form=tickets_form, auth=True, tickets=tickets)

        return render_template('tickets_form.html', title="AVHelpdesk", form=tickets_form, auth=False)

    @app.route('/ticket/<ticket_id>')
    def ticket(ticket_id):
        """
        Просмотр заявки.
        На этой странице сотрудник может просмотреть информацию по заявке и список всех сообщений, а также составить и
        отправить сообщение по заявке. Если проблема решена, то сотрудник закрывает заявку.
        """

        ticket = db.session.query(
            Ticket.id, Client.name, Staff.name, Ticket.created_date, TicketUrgency.urgency, Ticket.subject,
            Client.id, Client.email
            ).filter(
                Ticket.id == ticket_id
            ).join(
                Client, Client.id == Ticket.id_client
            ).outerjoin(
                Staff, Staff.id == Ticket.id_staff
            ).join(
                TicketUrgency, TicketUrgency.id == Ticket.id_urgency
            ).first()

        messages = db.session.query(Message.is_incoming, Message.content).filter(Message.id_ticket == ticket_id).all()
        ticket_form = TicketForm()

        return render_template(
            'ticket_form.html', title="AVHelpdesk", form=ticket_form, ticket=ticket, messages=messages
        )

    @app.route('/reply_ticket/<ticket_id>', methods=['POST'])
    def reply_ticket(ticket_id):
        """Отправка ответа по заявке"""

        ticket_form = TicketForm()
        message = ticket_form.reply.data
        ticket = db.session.query(Ticket).get(ticket_id)
        client = db.session.query(Client).get(ticket.id_client)
        check_subject = re.search(r'Helpdesk ticket \d+', ticket.subject)

        if check_subject is None:
            subject = f'Helpdesk ticket {ticket_id}: ' + ticket.subject

        message = send_email(client.email, subject, message, ticket_id, ticket.id_client)
        flash(message)

        return redirect(url_for('ticket', ticket_id=ticket_id))

    @app.route('/close_ticket/<ticket_id>')
    def close_ticket(ticket_id):
        """Закрытие заявки"""

        ticket = db.session.query(Ticket).get(ticket_id)
        ticket.id_status = CLOSED
        db.session.commit()

        return redirect(url_for('index'))

    @app.route('/get_email')
    def get_email():
        """Загрузка писем от клиентов. При работе с celery функция будет неактуальна"""

        messages = fetch_mail()
        add_ticket(messages)

        return 'Письма загружены'

    @app.route('/send')
    @login_required
    def email_form():
        """Форма отправки email"""
        if current_user.is_admin:
            form = SendForm()
            return render_template('email_form.html', title='Отправка email', form=form)

    @app.route('/email_process', methods=['POST'])
    def email_process():
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
    @login_required
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

        if current_user.is_admin:
            employees = db.session.query(
                Staff.id,
                Staff.name
            ).all()
        else:
            employees = [current_user]
        form = AssignForm()
        form.selection.choices = [(e.id, e.name) for e in employees]
        return render_template('tickets.html', title="Заявки", tickets=tickets, form=form)

    return app

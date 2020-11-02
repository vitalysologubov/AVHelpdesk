from flask import flash, Flask, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate
from sqlalchemy import and_
from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.forms import SendForm, LoginForm
from webapp.models import db, Staff, Ticket, TicketStatus, TicketUrgency
from webapp.send_email import send_email


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
        return Staff.query.get(user_id)

    @app.route('/')
    def index():
        """Главная страница: обработка входящих писем"""

        messages = fetch_mail()
        add_ticket(messages)

        return 'Работаем!'

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login_form.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Staff.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("You logged in")
                return redirect(url_for('index'))

            flash('Wrong username or password')
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

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

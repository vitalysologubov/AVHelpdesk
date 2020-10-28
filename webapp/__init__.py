from flask import flash,  Flask, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate
from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.forms import SendForm, LoginForm
from webapp.models import db, Staff
from webapp.send_email import send_email


def create_app():
    """Создание приложения"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    migrate = Migrate()
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(staff_id):
        return Staff.query.get(staff_id)

    @app.route('/')
    def index():
        """Главная страница: обработка входящих писем"""

        messages = fetch_mail()
        add_ticket(messages)

        return 'Работаем!'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login_form.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            staff_user = Staff.query.filter(Staff.login == login_form.login.data).first()
            if staff_user and staff_user.check_password(login_form.password.data):
                login_user(staff_user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
            flash('Неправильные реквизиты для входа')
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        flash('Вы вышли из личного кабинета')
        logout_user()
        return redirect(url_for('index'))

    @app.route('/send')
    @login_required
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

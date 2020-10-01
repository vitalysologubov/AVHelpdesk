from flask import Flask
from flask_migrate import Migrate
from webapp.add_tickets import add_ticket
from webapp.av_mail import fetch_mail
from webapp.models import db


def create_app():
    """Создание приложения"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        """Главная страница"""

        messages = fetch_mail()
        add_ticket(messages)

        return 'Работаем!'

    return app

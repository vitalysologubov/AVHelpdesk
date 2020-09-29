from flask import Flask
from flask_migrate import Migrate
from webapp.models import db


def create_app():
    """Создание приложения"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    Migrate(app, db)

    @app.route('/')
    def index():
        """Главная страница"""

        return 'Работаем!'

    return app

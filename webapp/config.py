import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))

# Путь к БД
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

# Отключение функционала отправки сигнала приложению при изменениях в БД,
# т.к. он создает большую дополнительную нагрузку на приложение
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SMTP
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    SECRET_KEY = os.getenv('SECRET_KEY')

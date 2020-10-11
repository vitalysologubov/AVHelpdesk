import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Путь к БД
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

# Отключение функционала отправки сигнала приложению при изменениях в БД,
# т.к. он создает большую дополнительную нагрузку на приложение
SQLALCHEMY_TRACK_MODIFICATIONS = False

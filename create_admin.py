from getpass import getpass
import sys

from webapp import create_app
from webapp.models import db, Staff

app = create_app()

with app.app_context():
    login = input('Login: ')
    if Staff.query.filter(Staff.login == login).count():
        print("Пользователь с таким логином уже есть")
        sys.exit(0)
    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')

    if not password == password2:
        print('Пароли не одинаковые')
        sys.exit(0)

    new_user = Staff(login=login)
    new_user.set_password(password2)
    db.session.add(new_user)
    db.session.commit()
    print(f"Пользователь {new_user.id} создан")

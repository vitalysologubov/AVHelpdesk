from getpass import getpass
import sys

from webapp import create_app
from webapp.models import db, Staff

app = create_app()
with app.app_context():
    username = input('Enter username:')
    if Staff.query.filter(Staff.username == username).count():
        print('User with the same username exists')
        sys.exit(0)
    password = getpass('Enter password:')
    password2 = getpass('Repeat password:')
    if not password == password2:
        print("Passwords don't match")
        sys.exit(0)
    new_user = Staff(username=username)
    new_user.set_password(password2)
    db.session.add(new_user)
    db.session.commit()
    print(f"User {new_user.id} created successfully")

from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Attachment(db.Model):
    """Вложения"""

    id = db.Column(db.Integer, primary_key=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    attachment = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, id_ticket={self.id_ticket}, attachment={self.attachment}'


class Client(db.Model):
    """Клиенты"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    organization = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, name={self.name}, organization={self.organization}, email={self.email}'


class Department(db.Model):
    """Отделы"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, name={self.name}'


class Staff(db.Model, UserMixin):
    """Сотрудники"""

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    id_department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True, default=None)
    name = db.Column(db.String, nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'id={self.id}, id_department={self.id_department}, name={self.name}, status={self.status}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 2


class Ticket(db.Model):
    """Заявки"""

    id = db.Column(db.Integer, primary_key=True)
    id_staff = db.Column(db.Integer, db.ForeignKey('staff.id'))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), nullable=False, default=1)
    id_urgency = db.Column(db.Integer, db.ForeignKey('ticket_urgency.id'), nullable=False, default=2)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)

    def __repr__(self):
        return (f'id={self.id}, id_staff={self.id_staff}, id_client={self.id_client}, id_status={self.id_status}, '
                f'id_urgency={self.id_urgency}, created_date={self.created_date}, subject={self.subject}, '
                f'content={self.content}')


class TicketStatus(db.Model):
    """Статусы заявок"""

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, status={self.status}'


class TicketUrgency(db.Model):
    """Срочность заявок"""

    id = db.Column(db.Integer, primary_key=True)
    urgency = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, urgency={self.urgency}'

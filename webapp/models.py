from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Attachment(db.Model):
    """Вложения"""

    id = db.Column(db.Integer, primary_key=True)
    id_message = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    attachment = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, id_ticket={self.id_message}, attachment={self.attachment}'


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
    id_department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'id={self.id}, id_department={self.id_department}, name={self.name}, status={self.status}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'Администратор'


class Ticket(db.Model):
    """Заявки"""

    id = db.Column(db.Integer, primary_key=True)
    id_staff = db.Column(db.Integer, db.ForeignKey('staff.id'))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), nullable=False, default=1)
    id_urgency = db.Column(db.Integer, db.ForeignKey('ticket_urgency.id'), nullable=False, default=2)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    subject = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    comments = db.Column(db.String)
    messages = db.relationship('Message', backref='ticket', lazy=True)

    @hybrid_property
    def full_subject(self):
        return f'Helpdesk ticket {self.id}: {self.subject}'

    def __repr__(self):
        return (f'id={self.id}, id_staff={self.id_staff}, id_client={self.id_client}, id_status={self.id_status}, '
                f'id_urgency={self.id_urgency}, created_date={self.created_date}, subject={self.subject}')


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


class Message(db.Model):
    """Письма"""

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    received_date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    is_incoming = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.String, nullable=False)
    attachments = db.relationship('Attachment', backref='message', lazy=True)

    def __repr__(self):
        return (f'id={self.id}', f'theme={self.theme}', f'id_client={self.id_client}',
                f'received_date={self.received_date}', f'is_incoming={self.is_incoming}', f'content={self.content}')

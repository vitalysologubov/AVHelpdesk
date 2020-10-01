from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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


class Departament(db.Model):
    """Отделы"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'id={self.id}, name={self.name}'


class Staff(db.Model):
    """Сотрудники"""

    id = db.Column(db.Integer, primary_key=True)
    id_departament = db.Column(db.Integer, db.ForeignKey('departament.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'id={self.id}, id_departament={self.id_departament}, name={self.name}, status={self.status}'


class Ticket(db.Model):
    """Заявки"""

    id = db.Column(db.Integer, primary_key=True)
    id_staff = db.Column(db.Integer, db.ForeignKey('staff.id'))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), nullable=False, default=1)
    id_urgency = db.Column(db.Integer, db.ForeignKey('ticket_urgency.id'), nullable=False, default=2)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.String)

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

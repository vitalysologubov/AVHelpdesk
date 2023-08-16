import argparse
import json

from webapp.models import Client, db, Department, Message, Staff, Ticket, TicketStatus, TicketUrgency
from webapp import create_app


parser = argparse.ArgumentParser(description='Добавление тестовых записей')
parser.add_argument('-c', '--client', help='Добавление клиентов')
parser.add_argument('-d', '--department', help='Добавление отделов')
parser.add_argument('-s', '--staff', help='Добавление сотрудников')
parser.add_argument('-ts', '--ticket_status', help='Добавление статусов заявок')
parser.add_argument('-tu', '--ticket_urgency', help='Добавление срочности заявок')
parser.add_argument('-t', '--ticket', help='Добавление заявок')
parser.add_argument('-m', '--message', help='Добавление сообщений из писем')
arguments = parser.parse_args()

app = create_app()

with app.app_context():
    if arguments.client:
        with open('fixtures/client.json', 'r', encoding='utf-8') as f:
            clients = json.load(f)[0]['records']

            for client in clients:
                data = Client(**client)
                db.session.add(data)

    elif arguments.department:
        with open('fixtures/department.json', 'r', encoding='utf-8') as f:
            departments = json.load(f)[0]['records']

            for department in departments:
                data = Department(**department)
                db.session.add(data)

    elif arguments.staff:
        with open('fixtures/staff.json', 'r', encoding='utf-8') as f:
            staffs = json.load(f)[0]['records']

            for staff in staffs:
                data = Staff(**staff)
                db.session.add(data)

    elif arguments.ticket_status:
        with open('fixtures/ticket_status.json', 'r', encoding='utf-8') as f:
            statuses = json.load(f)[0]['records']

            for status in statuses:
                data = TicketStatus(**status)
                db.session.add(data)

    elif arguments.ticket_urgency:
        with open('fixtures/ticket_urgency.json', 'r', encoding='utf-8') as f:
            urgency = json.load(f)[0]['records']

            for item in urgency:
                data = TicketUrgency(**item)
                db.session.add(data)

    elif arguments.ticket:
        with open('fixtures/ticket.json', 'r', encoding='utf-8') as f:
            tickets = json.load(f)[0]['records']

            for ticket in tickets:
                data = Ticket(**ticket)
                db.session.add(data)

    elif arguments.message:
        with open('fixtures/message.json', 'r', encoding='utf-8') as f:
            messages = json.load(f)[0]['records']

            for message in messages:
                data = Message(**message)
                db.session.add(data)

    db.session.commit()

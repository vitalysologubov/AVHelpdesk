import json
import argparse
from webapp.models import db, Client, Department, Staff, TicketStatus, TicketUrgency
from webapp import create_app

parser = argparse.ArgumentParser(description="Добавление тестовых записей")
parser.add_argument('-s', '--staff', help="Добавить только персонал")
parser.add_argument('-t', '--tickets', help="Добавить только данные заявок")
parser.add_argument('-a', '--all', help="Добавить все данные")
arguments = parser.parse_args()

print(arguments.staff)
print(arguments.tickets)

app = create_app()

with app.app_context():
    with open('fixtures/department.json', 'r', encoding='utf-8') as f:
        departments = json.load(f)[0]['records']

        for department in departments:
            data = Department(**department)
            db.session.add(data)

    with open('fixtures/staff.json', 'r', encoding='utf-8') as f:
        staffs = json.load(f)[0]['records']

        for staff in staffs:
            data = Staff(**staff)
            db.session.add(data)

    with open('fixtures/ticket_status.json', 'r', encoding='utf-8') as f:
        statuses = json.load(f)[0]['records']

        for status in statuses:
            data = TicketStatus(**status)
            db.session.add(data)

    with open('fixtures/ticket_urgency.json', 'r', encoding='utf-8') as f:
        urgency = json.load(f)[0]['records']

        for item in urgency:
            data = TicketUrgency(**item)
            db.session.add(data)
    
    if arguments.tickets:
        with open('fixtures/tickets.json', 'r', encoding='utf-8') as f:
            tickets = json.load(f)[0]['records']

            for ticket in tickets:
                data = TicketStatus(**ticket)
                db.session.add(data)

    db.session.commit()

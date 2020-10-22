import json
from webapp.models import db, Client, Department, Staff, TicketStatus, TicketUrgency
from webapp import create_app


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

    db.session.commit()

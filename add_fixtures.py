import json
from webapp.models import db, Client, Departament, Staff, TicketStatus, TicketUrgency
from webapp import create_app


app = create_app()

with app.app_context():
    with open('fixtures/client.json', 'r', encoding='utf-8') as f:
        clients = json.load(f)[0]['records']

        for client in clients:
            data = Client(**client)
            db.session.add(data)

    with open('fixtures/departament.json', 'r', encoding='utf-8') as f:
        departaments = json.load(f)[0]['records']

        for departament in departaments:
            data = Departament(**departament)
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

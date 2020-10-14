import re
from flask_sqlalchemy import sqlalchemy
from webapp.models import db, Client, Message, Ticket


def get_or_create_client_by_email(name, email):
    """Проверка наличия клиента в БД"""

    try:
        client = Client.query.filter(Client.email == email).one()
    except sqlalchemy.orm.exc.NoResultFound:
        client = Client(name=name, email=email)
        db.session.add(client)
        db.session.commit()

    return client


def add_ticket(messages):
    """
    Создание заявки на основе письма, полученного от клиента, и сохранение письма в БД.
    Если тема письма не содержит строку "Helpdesk ticket <ticket_id>, то создаётся новая заявка и добавляется письмо,
    привязанное к этой заявке.
    Если тема письма содержит такую строку, то из неё извлекается ИД заявки и добавляется письмо, привязанное к нужной
    заявке.
    """

    for message in messages:
        is_initial_email = re.search(r'Helpdesk ticket \d+', message['subject'])

        if is_initial_email is None:
            client_id = get_or_create_client_by_email(message['author'], message['address']).id           
            task = Ticket(id_client=client_id, subject=message['subject'], description=message['body'])

            try:
                db.session.add(task)
                db.session.commit()
                ticket_id = task.id
            except sqlalchemy.exc.OperationalError as error:
                ticket_id = ""
                print(f'Не удалось создать заявку от {message["address"]} с темой {message["subject"]}: {error}')
        else:
            subject = is_initial_email.group(0)
            ticket_id = re.search(r'\d+', subject).group(0)
            client_id = Ticket.query.filter(Ticket.id == ticket_id).first().id_client

        if ticket_id:
            add_email(message["subject"], client_id, ticket_id, message['body'])


def add_email(subject, client_id, ticket_id, content):
    """Добавление письма"""

    email = Message(theme=subject, id_client=client_id, id_ticket=ticket_id, is_incoming=True, content=content)

    try:
        db.session.add(email)
        db.session.commit()
    except sqlalchemy.exc.OperationalError as error:
        print(f'Не удалось добавить письмо от {message["address"]} с темой {message["subject"]}: {error}')

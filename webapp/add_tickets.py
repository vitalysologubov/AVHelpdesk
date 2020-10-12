from flask_sqlalchemy import sqlalchemy
from webapp.models import db, Client, Ticket


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
    """Добавление заявки на основе письма"""

    for message in messages:
        client = get_or_create_client_by_email(message['author'], message['address'])
        task = Ticket(id_client=client.id, subject=message['subject'], content=message['body'])

        try:
            db.session.add(task)
            db.session.commit()
        except sqlalchemy.exc.OperationalError as error:
            print(f'Не удалось создать заявку от {message["address"]} с темой {message["subject"]}: {error}')

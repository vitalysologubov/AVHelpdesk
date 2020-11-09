import smtplib
import socket
import ssl
from flask_sqlalchemy import sqlalchemy
from webapp.config import EMAIL_PASSWORD, EMAIL_SENDER, SMTP_SERVER
from webapp.models import db, Message


def create_body(receiver, subject, message):
    """Создание сообщения"""

    body = "\r\n".join((
        "From: %s" % EMAIL_SENDER,
        "To: %s" % receiver,
        "Subject: %s" % subject,
        "",
        message)).encode('utf-8')

    return body


def save_email(subject, client_id, ticket_id, content):
    """Сохранение сообщения в БД"""

    message = Message(theme=subject, id_client=client_id, id_ticket=ticket_id, is_incoming=0, content=content)

    try:
        db.session.add(message)
        db.session.commit()
    except sqlalchemy.exc.OperationalError as error:
        print(f'Не удалось добавить ответ для заявки с темой {subject}: {error}')


def send_email(receiver, subject, message, ticket_id, client_id):
    """Отправка сообщения"""

    context = ssl.create_default_context()
    body = create_body(receiver, subject, message)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, [receiver], body)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused, socket.gaierror) as error:
        return f'Ошибка отправки сообщения: {error}'

    save_email(subject, client_id, ticket_id, message)
    return 'Сообщене отправлено'

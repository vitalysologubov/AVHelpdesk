import smtplib
import socket
import ssl
from flask_sqlalchemy import sqlalchemy

from webapp.config import EMAIL_PASSWORD, EMAIL_SENDER, SMTP_SERVER
from webapp.models import db, Message


def create_body(email, subject, content):
    """Создание сообщения"""

    body = '\r\n'.join((
        'From: %s' % EMAIL_SENDER,
        'To: %s' % email,
        'Subject: %s' % subject,
        '',
        content)).encode('utf-8')

    return body


def save_email(client_id, ticket_id, subject, content):
    """Сохранение сообщения в БД"""

    message = Message(id_client=client_id, id_ticket=ticket_id, is_incoming=False, subject=subject, content=content)

    try:
        db.session.add(message)
        db.session.commit()
    except sqlalchemy.exc.OperationalError as error:
        print(f'Не удалось добавить ответ на заявку с темой {subject}: {error}')


def send_email(ticket_id, client_id, email, subject, content):
    """Отправка сообщения"""

    context = ssl.create_default_context()
    body = create_body(email, subject, content)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, [email], body)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused, socket.gaierror) as error:
        return f'Ошибка отправки сообщения: {error}'

    save_email(client_id, ticket_id, subject, content)
    return 'Сообщене отправлено'

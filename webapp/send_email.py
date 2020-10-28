import smtplib
import socket
import ssl
from webapp.config import SMTP_PASSWORD, SMTP_SERVER, EMAIL_SENDER


def create_body(receiver, subject, message):
    """Создание сообщения"""

    body = "\r\n".join((
        "From: %s" % EMAIL_SENDER,
        "To: %s" % receiver,
        "Subject: %s" % subject,
        "",
        message)).encode('utf-8')

    return body


def send_email(receiver, subject, message):
    """Отправка email"""

    context = ssl.create_default_context()
    body = create_body(receiver, subject, message)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, context=context) as smtp:
            smtp.login(EMAIL_SENDER, SMTP_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, [receiver], body)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused, socket.gaierror) as error:
        return f'Ошибка отправки сообщения: {error}'

    return 'Сообщение отправлено'

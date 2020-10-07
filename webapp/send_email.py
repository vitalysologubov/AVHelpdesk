import smtplib
import socket
import ssl
from webapp.config import EMAIL_SENDER, SMTP_PASSWORD, SMTP_SERVER


def send_email(receiver, subject, message):
    """Отправка email"""

    body = "\r\n".join((
        "From: %s" % EMAIL_SENDER,
        "To: %s" % receiver,
        "Subject: %s" % subject,
        "",
        message)).encode('utf-8')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, context=context) as smtp:
            smtp.login(EMAIL_SENDER, SMTP_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, [receiver], body)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused, socket.gaierror) as error:
        return f'Ошибка отправки сообщения: {error}'

    return 'Сообщене отправлено'

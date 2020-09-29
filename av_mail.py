import os
from dotenv import load_dotenv
import email
import imaplib
from email.header import decode_header
from bs4 import BeautifulSoup


def remove_tags(html_code):
    """
    Удаление тегов и очистка текста
    """
    soup = BeautifulSoup(html_code, 'html.parser')
    result: str = soup.get_text()
    result = result.replace('\n', ' ')
    result = result.replace('\r', ' ')
    result = result.replace('\xa0', ' ')
    while '  ' in result:
        result = result.replace('  ', '')
    return result


def decode_mail_header(raw_header):
    d = decode_header(raw_header)
    subject, encoding = d[0]
    subject = subject.decode(encoding)
    return subject


def multipart(message):
    result = None
    if not message.is_multipart():
        result = message.get_payload(decode=True).decode('utf-8')
    else:
        for payload in message.get_payload():
            return multipart(payload)
    if result:
        return result


def fetch_mail():
    # https://www.dmosk.ru/instruktions.php?object=python-mail
    msg_list = []
    mail = get_mailbox_entity()
    # search criteria https://gist.github.com/martinrusev/6121028
    result, data = mail.search(None, "UNSEEN")

    ids = data[0]
    id_list = ids.split()
    for email_id in id_list[::-1]:
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        address = email.utils.parseaddr(email_message['From'])[1]
        message_content = {
            'headers': (
                f"{address}",
                f"{decode_mail_header(email_message['From'])}",
                f"{email_message['Date']}",
                f"{decode_mail_header(email_message['Subject'])}"
            )
        }
        body = ''
        if email_message.is_multipart():
            for payload in email_message.get_payload():
                body += multipart(payload)
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')
        message_content['body'] = remove_tags(body)
        msg_list.append(message_content)


def get_mailbox_entity():
    """
    Подключение к почтовому ящику
    """
    _mail = None
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        ssl_address = os.getenv('SSL_ADDRESS')
        email_login = os.getenv('EMAIL_LOGIN')
        email_password = os.getenv('EMAIL_PASSWORD')
        _mail = imaplib.IMAP4_SSL(ssl_address)
        _mail.login(email_login, email_password)
        _mail.select("inbox")
    return _mail


def is_needs_to_decode(payload_data):
    """
    Определение, нужно ли декодировать тело письма
    """

    is_encoded_text = (
        not payload_data.strip() or
        not payload_data.isascii() or
        ' ' in payload_data or '&nbsp;' in payload_data or
        payload_data.isalpha() or payload_data.isdigit()
        )
    if is_encoded_text:
        return False
    else:
        return True


def obtain_html_body(message):
    """
    Получить тело письма
    """
    body = []
    if message.is_multipart():
        for payload in message.get_payload():
            new_part = obtain_html_body(payload).strip()
            if new_part not in body:
                body.append(new_part)
        return remove_tags(" ".join(body))
    else:
        if not is_needs_to_decode(message.get_payload()):
            return remove_tags(message.get_payload())
        else:
            return remove_tags(message.get_payload(decode=True).decode('utf-8'))


def fetch_mail():
    """
    Проход по почтовым сообщениям
    """
    msg_list = []
    mail = get_mailbox_entity()
    # search criteria https://gist.github.com/martinrusev/6121028
    result, data = mail.search(None, "UNSEEN")
    id_list = (i for i in data[0].split()[::-1] if not i == ' ')
    for email_id in id_list:
        r_, message_data = mail.fetch(email_id, "(RFC822)")
        raw_email_message = message_data[0][1]
        print(f'{raw_email_message=}')
        raw_email_message_string = raw_email_message.decode('utf-8')
        email_message = email.message_from_string(raw_email_message_string)
        address = email.utils.parseaddr(email_message['From'])[1]
        body = obtain_html_body(email_message)
        mcd = dict(
            address=address,
            author=decode_mail_header(email_message['From']),
            received=email_message['Date'],
            subject=decode_mail_header(email_message['Subject']),
            body=body
        )
        msg_list.append(mcd)
    return msg_list

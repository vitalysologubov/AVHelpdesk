import pytest
from unittest import mock, TestCase
from webapp import av_mail
from webapp import create_app
from webapp.add_tickets import add_ticket, get_or_create_client_by_email
from webapp.models import Message
from webapp.send_email import send_email


app = create_app()


class TestSendEmail(TestCase):
    """Тестирование отправки email"""

    @mock.patch('smtplib.SMTP_SSL')
    def test_send_email(self, mock_send_email):
        with app.app_context():
            result = send_email('test@client.com', 'TestSubject', 'TestMessage', 1, 1)
            assert result == 'Сообщене отправлено'


@pytest.fixture
def client():
    """Получение данных клиента"""

    with app.app_context():
        return get_or_create_client_by_email('Иван Иванов', 'ivan@ivanov.ru')


def test_client(client):
    """Тестирование клиента"""

    with app.app_context():
        assert client.name == 'Иван Иванов'
        assert client.email == 'ivan@ivanov.ru'


@pytest.fixture
def messages():
    """Сообщения электронной почты"""

    messages = [
        {
            'address': 'ivanov@sender.com',
            'author': 'Ivan Ivanov',
            'received': 'Thu, 8 Oct 2020 21:24:58 +0300',
            'subject': 'Test subject 1',
            'body': 'Test content 1',
            'attachments': ['20201221171254_eu56veqr26.txt']
        },
        {
            'address': 'petrov@sender.com',
            'author': 'Petr Petrov',
            'received': 'Thu, 8 Oct 2020 22:11:45 +0300',
            'subject': 'Test subject 2',
            'body': 'Test content 2',
            'attachments': ['20201221171254_eu56veqr27.txt']
        }
    ]

    return messages


def test_add_email(messages):
    """Тестирование добавления писем"""

    with app.app_context():
        av_mail.fetch_mail = mock.MagicMock(return_value=messages)
        messages = av_mail.fetch_mail()
        add_ticket(messages)

        for message in messages:
            email = Message.query.filter(
                Message.theme == message['subject'], Message.content == message['body']
            ).order_by(Message.id.desc()).first()

            assert message['subject'] == email.theme
            assert message['body'] == email.content

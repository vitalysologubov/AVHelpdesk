from flask import Flask, Response
from webapp.av_mail import fetch_mail
app = Flask(__name__)


@app.route('/about')
def index():
    return 'Main page of AVHelpdesk'


@app.route('/')
def obtain_mail():
    messages = fetch_mail()
    output = ''
    if messages:
        for message in messages:
            for field in message.keys():
                output += message[field] + '<br/>'
            output += '<br/><br/>'
        return Response(output)
    else:
        return Response('Нет новых сообщений')


if __name__ == '__main__':
    app.run()

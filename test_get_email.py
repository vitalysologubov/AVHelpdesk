import pytest
from webapp import get_email


@pytest.fixture
def message_generator():
    """Генератор сообщений"""

    raw_email_string = b'''Received: from mxfront7g.mail.yandex.net (localhost [127.0.0.1])\r\n\t
    by mxfront7g.mail.yandex.net with LMTP id vu4jZ3bEoi-xn3f2MQM\r\n\t
    for <av-helpdesk@yandex.ru>; Sat, 26 Sep 2020 14:40:32 +0300\r\n
    Received: from mail-wm1-x333.google.com (mail-wm1-x333.google.com [2a00:1450:4864:20::333])\r\n\t
    by mxfront7g.mail.yandex.net (mxfront/Yandex) with ESMTPS id n6HIeR7zil-eVau8PVJ;\r\n\t
    Sat, 26 Sep 2020 14:40:31 +0300\r\n\t
    (using TLSv1.3 with cipher TLS_AES_256_GCM_SHA384 (256/256 bits))\r\n\t
    (Client certificate not present)\r\n
    Return-Path: da070116@gmail.com\r\n
    X-Yandex-Front: mxfront7g.mail.yandex.net\r\n
    X-Yandex-TimeMark: 1601120431.832\r\n

    Authentication-Results: mxfront7g.mail.yandex.net;
    spf=pass (mxfront7g.mail.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::333 as permitted sender, 
    rule=[ip6:2a00:1450:4000::/36]) smtp.mail=da070116@gmail.com; dkim=pass header.i=@gmail.com\r\n

    X-Yandex-Suid-Status: 1 1543103945\r\n
    X-Yandex-Spam: 1\r\n
    X-Yandex-Fwd: MTY2MzA3NTQwMzU2MDAwMzgwOTEsNzExMjA5MTQ4MjUyMTg4NDcyNA==\r\n
    Received: by mail-wm1-x333.google.com with SMTP id k18so1965729wmj.5\r\n
    for <av-helpdesk@yandex.ru>; Sat, 26 Sep 2020 04:40:31 -0700 (PDT)\r\n
    DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n
    d=gmail.com; s=20161025;\r\n
    h=mime-version:from:date:message-id:subject:to;\r\n
    bh=bdtMCJlcxVtlZS7gaOaHOhugDXJBI4dVo2yTvyW8qg8=;\r\n
    b=WW3wEv4kZ1/xtRktepKsfNiUxBjMeGeJSyRWhrcybobMsoacoDqdNqLlLickhSd026\r\n
    gvYSTJ6TPXcgVrfJlM+2cfTzGgB6cAs9C5RyMoH/HRoiuJojDfX0ISpqYRDaIiQYRLiI\r\n
    DJD6R/Vs7uAap/sLcwMpe+jIdsg2NFN3VvPXXeCkmwXixuq1B3aOVhsCJHUYRNFCl/Pw\r\n
    NtIUauoQPXBmEitvt+N20GDCjXs8DQSAA4FxvnCHzVkudCWXwQrP3XMEdK3iHLwQgx1b\r\n
    bR0KIg9awpJevlvHzwMNA1Fz8vQGdH9/10Phn0L+JdEzzBZMZzZLxkUTIV0YK5YkQ6pn\r\n
    srbg==\r\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n
    d=1e100.net; s=20161025;\r\n
    h=x-gm-message-state:mime-version:from:date:message-id:subject:to;\r\n
    bh=bdtMCJlcxVtlZS7gaOaHOhugDXJBI4dVo2yTvyW8qg8=;\r\n
    b=jOP+MuTgrFJXze+ksShsmXEfwvXcEIFSERDpHwplQczRFkWOxzFaopZBKb9WnrvjE5\r\n
    TTZerY5uwBR6qVeAfBJErp3S5JwSj9OySaE7nOOuyGIn1JzEYgqsl3Ki/YTVszYVkNHx\r\n
    hYYXmg/jHNs8nodD/UnqjdotsYso7BAyGzzVvBA2Me4/U+gxMvbOJZRATNabJ0z5q6ft\r\n
    cS02oO7mGKv9XxuTPqS+fnCPyovHuyJvUSBBqxB27M0PX2020pEheWxlDOA7H3r28xEO\r\n
    Kzd/+avzEGn/bEcTw46pvk0FGreVjf38OXD2/yJnjY7onA76MniHZ8vAPuk2y0bTvuzo\r\n
    kgWQ==\r\nX-Gm-Message-State: AOAM530Q4dX0yrKDP5BVeXOa+X1E0DFAB4PLWQSn/rwlaL5KFdsDIONU\r\n\
    tiHtdqZgYgS8jb7pltFwYmsOZdshSqkdyfnfrB/LZVjoi\r\n
    X-Google-Smtp-Source: ABdhPJxqT7XPlUW596xJqCQW4ps0XZ4EvS9wsuOtdZ/ygaJxVLvgXsvE5OodHtg0k0ezbgdHQW6e1vxeUN+EINVVNng=\r\n
    X-Received: by 2002:a1c:4d12:: with SMTP id o18mr2392596wmh.177.1601120431518;\r\n
    Sat, 26 Sep 2020 04:40:31 -0700 (PDT)\r\nMIME-Version: 1.0\r\n
    From: Alexander D <da070116@gmail.com>\r\n
    Date: Sat, 26 Sep 2020 14:40:19 +0300\r\n
    Message-ID: <CAKVU9xtzT35Xx0Ez0YunGDA7umOJ0ffv_8U8ramDB-FBhE4ntw@mail.gmail.com>\r\n
    Subject: =?UTF-8?B?0KLQtdGB0YI=?=\r\n
    To: av-helpdesk@yandex.ru\r\n
    Content-Type: multipart/alternative; boundary="000000000000903a2405b035e668"\r\n
    X-Yandex-Forward: ab6645c55ffdccbee52bce170ab86e30\r\n\r\n--000000000000903a2405b035e668\r\n
    Content-Type: text/plain; charset="UTF-8"\r\nContent-Transfer-Encoding: base64\r\n\r\n
    0KLQtdGB0YINCg==\r\n
    --000000000000903a2405b035e668\r\n
    Content-Type: text/html; charset="UTF-8"\r\n
    Content-Transfer-Encoding: base64\r\n\r\n
    PGRpdiBkaXI9Imx0ciI+0KLQtdGB0YI8YnI+PC9kaXY+DQo=
    \r\n--000000000000903a2405b035e668--\r\n'''
    email_message = ''
    return email_message


@pytest.fixture
def mail_connection():
    """Получение параметров подключения"""

    import os
    import imaplib
    from dotenv import load_dotenv
    mail = None
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        ssl_address = os.getenv('SSL_ADDRESS')
        email_login = os.getenv('EMAIL_LOGIN')
        email_password = os.getenv('EMAIL_PASSWORD')
        mail = imaplib.IMAP4_SSL(ssl_address)
        mail.login(email_login, email_password)
        mail.select("inbox")
    return mail


def test_get_mailbox_entity():
    """Тестирование подключения"""

    entity = get_email.get_mailbox_entity()
    assert entity.noop() == ('OK', [b'NOOP Completed.'])


def test_is_needs_to_decode():
    """Тестирование необходимости декодирования тела письма"""

    cyrillic_many_words = "Привет, мир!"
    cyrillic_one_word = "Привет!"
    latin_many_words = "Hello world!"
    latin_one_word = "Hello!"
    encoded_string = """0J/RgNC40LLQtdGCLCDQvNC40YAh"""
    empty_string = ""
    spaced_string = "    "
    assert get_email.is_needs_to_decode(cyrillic_many_words) is False
    assert get_email.is_needs_to_decode(cyrillic_one_word) is False
    assert get_email.is_needs_to_decode(latin_many_words) is False
    assert get_email.is_needs_to_decode(latin_one_word) is False
    assert get_email.is_needs_to_decode(empty_string) is False
    assert get_email.is_needs_to_decode(spaced_string) is False
    assert get_email.is_needs_to_decode(encoded_string) is True


def test_obtain_html_body():
    """Тестирование получения тела письма"""

    cyrillic_many_words = "Привет, мир!"
    cyrillic_one_word = "Привет!"
    latin_many_words = "Hello world!"
    latin_one_word = "Hello!"
    encoded_string = """0J/RgNC40LLQtdGCLCDQvNC40YAh"""
    mail = mail_connection
    result, data = mail.search(None, "UNSEEN")
    id_list = (i for i in data[0].split()[::-1] if not i == ' ')
    print(get_email.obtain_html_body(cyrillic_many_words))

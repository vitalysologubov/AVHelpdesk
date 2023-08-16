from celery import Celery
from celery.schedules import crontab
from server import obtain_mail


celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.on_after_configure.connect
def periodic_mail_receive(sender, **kwargs):
    sender.add_periodic_task(16.0, obtain_mail.s())


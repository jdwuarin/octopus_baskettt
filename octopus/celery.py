from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octopus.settings')

app = Celery('octopus')

app.config_from_object('django.conf:settings')

if __name__ == '__main__':
    app.start()
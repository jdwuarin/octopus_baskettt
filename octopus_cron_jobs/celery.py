from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octopus.settings')

app = Celery('octopus_cron_jobs',
             broker='amqp://octopus_rabbitmq_user:octopus_rabbitmq_password@octopus-crawler/octopus_rabbitmq_vhost',
             backend='amqp://octopus_rabbitmq_user:octopus_rabbitmq_password@octopus-crawler/octopus_rabbitmq_vhost',
             include=['octopus_cron_jobs.tasks'],)

app.config_from_object('octopus.celeryconfig')

if __name__ == '__main__':
    app.start()
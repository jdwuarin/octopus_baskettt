from __future__ import absolute_import
from django.conf import settings
from celery import Celery

app = Celery('octopus_automation',
             broker='amqp://octopus_rabbitmq_user:octopus_rabbitmq_password@octopus-crawler/octopus_rabbitmq_vhost',
             backend='amqp://octopus_rabbitmq_user:octopus_rabbitmq_password@octopus-crawler/octopus_rabbitmq_vhost',
             include=['octopus_automation.tasks'])

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'create_recommendations_then_email': {
        'task': 'tasks.create_recommendations_then_email',
        'schedule': crontab(minute='*/1'),
    },

    'sanitize_db': {
        'task': 'tasks.sanitize_db',
        'schedule': crontab(minute=0, hour='*/3'),
    },
}

CELERY_TIMEZONE='Europe/London'
CELERY_ENABLE_UTC=True

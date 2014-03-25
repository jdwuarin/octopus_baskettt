from octopus.celery import app
from octopus_cron_jobs import sanitize_database
from octopus_cron_jobs import recommendations_email

@app.task
def create_recommendations_then_send_email():
    recommendations_email.create_recommendations_then_send_email()

@app.task
def sanitize_db():
    sanitize_database.clean_user_settings()
    sanitize_database.set_in_stock_flag()
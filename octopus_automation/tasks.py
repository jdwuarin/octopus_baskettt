from octopus_automation.celery import app
from octopus_automation import sanitize_db
from octopus_automation import recommendations_email

@app.task
def create_recommendations_then_send_email():
    recommendations_email.create_recommendations_then_send_email()

@app.task
def sanitize_db():
    sanitize_db.clean_user_settings()
    sanitize_db.set_in_stock_flag()
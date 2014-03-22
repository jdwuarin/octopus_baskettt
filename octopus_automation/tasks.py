from octopus_automation.celery import app
from octopus_automation import sanitize_database

@app.task
def sanitize_db(x, y):
    sanitize_database.clean_user_settings()
    sanitize_database.set_in_stock_flag()
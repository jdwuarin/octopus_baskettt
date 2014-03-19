from octopus_user.models import *
from datetime import datetime
from datetime import timedelta

def recommendation_automation():

    #go through all user_settings and only take the one that have an attached user
    clean_user_settings()

    pass

def clean_user_settings():
    user_settings_list = UserSettings.objects.all()

    three_days = timedelta(days=3)
    for user_settings in user_settings_list:
        if not user_settings.user and (
                    datetime.now() - user_settings.time > three_days):
            user_settings.delete()
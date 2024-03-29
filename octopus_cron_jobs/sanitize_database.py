from octopus_groceries.models import Product
from octopus_user.models import *
from datetime import datetime
from datetime import timedelta

two_weeks = timedelta(days=14)


def clean_user_settings():
    user_settings_list = UserSettings.objects.all()

    for user_settings in user_settings_list:
        if not user_settings.user and (
                    datetime.now() - user_settings.created_at > two_weeks):
            user_settings.delete()

# set flag to false if product was not found in last crawl (essentially)
# TODO still need to deal with what happens if producer site is down during crawl
# and all products get set to out of stock...


def set_in_stock_flag():
    pass
    #products = Product.objects.all()

    # this does not seem to be true, so...

    #for product in products:
    #    if datetime.now() - product.updated_at > one_day:
    #        product.in_stock = False
    #        product.save()
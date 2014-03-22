from octopus_groceries.models import Products
from octopus_user.models import *
from datetime import datetime
from datetime import timedelta

one_day = timedelta(days=1)

def clean_user_settings():
    user_settings_list = UserSettings.objects.all()

    for user_settings in user_settings_list:
        if not user_settings.user and (
                    datetime.now() - user_settings.time > one_day):
            user_settings.delete()

# set flag to false if product was not found in last crawl (essentially)
# TODO still need to deal with what happens if producer site is down during crawl
# and all products get set to out of stock...
def set_in_stock_flag():
    products = Product.object.all()

    for product in products:
        if datetime.now() - product.updated_at > one_day:
            product.in_stock = False
            product.save()
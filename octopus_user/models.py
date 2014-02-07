from django.db import models
from django.contrib.auth.models import User
from octopus_groceries.models import Product
from django_hstore import hstore

class UserSettings(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    people = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    # value from 0 to 1. 0 completely insensitive, 1 extremely sensitive
    price_sensitivity = models.DecimalField(max_digits=10, decimal_places=4)
    budget = models.DecimalField(max_digits=10, decimal_places=4)
    tags = models.CommaSeparatedIntegerField(max_length=5000, default=[])

# basket that was recommended to our user by our algorithm
class UserRecommendedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    product_dict = hstore.DictionaryField()  # product_id's mapped to quantities
    time = models.DateField(default=0, auto_now=True)

    objects = hstore.HStoreManager()


# basket that was finally transferred to the supermarket
# (before items failed being transferred etc)
# saving commaSeperatedValues: user_generated_basket =
class UserGeneratedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    user_recommended_basket = models.OneToOneField(UserRecommendedBasket,
                                                   primary_key=True)
    product_dict = hstore.DictionaryField()
    time = models.DateField(default=0, auto_now=True)

    objects = hstore.HStoreManager()


class UserProductSlack(models.Model):
    user = models.ForeignKey(User, editable=False)
    product = models.ForeignKey(Product, editable=False)
    slack = models.DecimalField(max_digits=10, decimal_places=4, editable=True)
    purchase_time = models.DateField(default=0, auto_now=True)


class UserInvited(models.Model):
    email = models.CharField(max_length=150, editable=False, primary_key=True)
    is_invited = models.NullBooleanField(editable=True)



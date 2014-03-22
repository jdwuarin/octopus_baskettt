from django.db import models
import datetime
from django.contrib.auth.models import User
from octopus_groceries.models import *
from django_hstore import hstore


class UserSettings(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    people = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    # value from 0 to 1. 0 completely insensitive, 1 extremely sensitive
    price_sensitivity = models.DecimalField(max_digits=10, decimal_places=4)
    tags = models.CommaSeparatedIntegerField(max_length=5000, default=[])
    default_supermarket = models.ForeignKey(
        Supermarket,default=None, blank=True, null=True, editable=False)
    pre_user_creation_hash = models.CharField(
        max_length=150, default='', editable=False, blank=True, null=True,
        db_index=True)

    # email subscription bullshit stuff.
    recommendation_email_subscription = models.BooleanField(default=True)
    news_email_subscription = models.BooleanField(default=True)

    diet = models.ForeignKey(Diet, blank=True, null=True)
    banned_meats = models.CommaSeparatedIntegerField(
        max_length=5000, default=[])  # id list of BannableMeats
    banned_abstract_products = models.CommaSeparatedIntegerField(
        max_length=5000, default=[])  # id list of AbstractProducts

    created_at = models.DateTimeField(auto_now_add=True,
                                      default=datetime.datetime.now())

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.people) + ", " + str(
            self.days) + ", " + str(
            self.price_sensitivity) + ", " + str(
            self.tags) + ", " + str(
            self.diet) + ", " + str(
            self.default_supermarket) + ", " + str(
            self.banned_meats) + ", " + str(
            self.banned_abstract_products)


# basket that was recommended to our user by our algorithm
class UserRecommendedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    product_dict = hstore.DictionaryField()  # product_id's mapped to quantities
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                auto_now_add=True)

    objects = hstore.HStoreManager()


# basket that was finally transferred to the supermarket
# (before items failed being transferred etc)
# saving commaSeperatedValues: user_generated_basket =
class UserGeneratedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    user_recommended_basket = models.OneToOneField(UserRecommendedBasket,
                                                   primary_key=True)
    product_dict = hstore.DictionaryField()
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                auto_now_add=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.user_recommended_basket.id) + ", " + str(
            self.product_dict) + ", " + str(
            self.time)


class UserProductSlack(models.Model):
    user = models.ForeignKey(User, editable=False)
    product = models.ForeignKey(Product, editable=False)
    slack = models.DecimalField(max_digits=10, decimal_places=4, editable=True)
    purchase_time = models.DateTimeField(default=datetime.datetime.now(),
                                         auto_now_add=True)


class UserInvited(models.Model):
    email = models.CharField(max_length=150, editable=False, primary_key=True)
    is_invited = models.NullBooleanField(editable=True)
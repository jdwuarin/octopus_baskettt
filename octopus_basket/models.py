from django.db import models
from django.conf import settings
from django_hstore import hstore
import datetime


class AvailableTag(models.Model):  # for baskets (like recipe, vegan, vegetarian etc...)
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class UserBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    parent = models.ForeignKey('self', blank=True, default=None)
    description = models.TextField(blank=True, default='')
    product_dict = hstore.DictionaryField()  # product_id's mapped to quantities
    people = models.IntegerField(default=1)
    hash = models.CharField(max_length=60, blank=True, default=None,
                            db_index=True)
    # to generate it:
    # user_hash = ''.join(random.choice(
    #     string.ascii_letters + string.digits) for x in range(60))

    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.name) + ", " + str(
            self.description) + ", " + str(
            self.created_at)


class UserBasketTag(models.Model):
    tag = models.ForeignKey(AvailableTag, blank=False)
    user_basket = models.ForeignKey(UserBasket)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_basket)


class UserCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    parent = models.ForeignKey('self', blank=True, default=None)
    description = models.TextField(blank=True, default='')
    basket_list = models.CommaSeparatedIntegerField(max_length=60)
    people = models.IntegerField(default=1)
    hash = models.CharField(max_length=60, blank=True, default=None,
                            db_index=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now=True)

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.name) + ", " + str(
            self.description) + ", " + str(
            self.created_at)


class UserCartTag(models.Model):
    tag = models.ForeignKey(AvailableTag, blank=False)
    user_cart = models.ForeignKey(UserCart)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_cart)

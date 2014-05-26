from django.db import models
from django.conf import settings
from django_hstore import hstore
import datetime


class AvailableTag(models.Model):  # for baskets (like recipe, vegan, vegetarian etc...)
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    parent = models.ForeignKey('self', blank=True, default=None,
        null=True)
    description = models.TextField(blank=True, default='')
    product_dict = hstore.DictionaryField()  # product_id's mapped to query term and quantities
    hash = models.CharField(max_length=60, blank=True, default=None,
                            primary_key=True, db_index=True)
    is_public = models.BooleanField(null=False, blank=False, default=False)
    is_browsable = models.BooleanField(null=False, blank=False, default=False)
    purchase_count = models.IntegerField(null=False, blank=False, default=0)
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


class BasketTag(models.Model):
    tag = models.ForeignKey(AvailableTag, blank=False)
    basket = models.ForeignKey(Basket)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_basket)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    parent = models.ForeignKey('self', blank=True, default=None,
        null=True)
    description = models.TextField(blank=True, default='')
    basket_list = models.CommaSeparatedIntegerField(max_length=60)
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
    user_cart = models.ForeignKey(Cart)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_cart)

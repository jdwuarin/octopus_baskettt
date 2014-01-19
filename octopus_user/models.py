from django.db import models
from django.contrib.auth.models import User
from octopus_groceries.models import Product, AbstractProduct

class UserSettings(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    num_people = models.IntegerField(editable=False)
    num_days = models.IntegerField(editable=False)
    budget = models.DecimalField(max_digits=10, decimal_places=4, editable=True)

#basket that was recommended to our user by our algorithm
class UserRecommendedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    product_list = models.CommaSeparatedIntegerField(max_length=5000)
    quantity_list = models.CommaSeparatedIntegerField(max_length=5000)
    time = models.DateField(default=0, auto_now=True)


#basket that was finally transferred to the supermarket (before items failed being transferred etc)
#saving commaSeperatedValues: user_generated_basket =
class UserGeneratedBasket(models.Model):
    user = models.ForeignKey(User, editable=False)
    user_recommended_basket = models.OneToOneField(UserRecommendedBasket, primary_key=True)
    product_list = models.CommaSeparatedIntegerField(max_length=5000)  # just set to a list of product_ids to that.
    quantity_list = models.CommaSeparatedIntegerField(max_length=5000)
    time = models.DateField(default=0, auto_now=True)


class UserProductSlack(models.Model):
    user = models.ForeignKey(User, editable=False)
    product = models.ForeignKey(Product, editable=False)
    slack = models.DecimalField(max_digits=10, decimal_places=4, editable=True)
    purchase_time = models.DateField(default=0, auto_now=True)

class UserInvited(models.Model):
    email = models.CharField(max_length=150, editable=False, primary_key=True)
    is_invited = models.NullBooleanField(editable=True)



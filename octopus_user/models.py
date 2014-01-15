from django.db import models
from django.contrib.auth.models import User
from octopus_groceries.models import Product, AbstractProduct

class UserPreferences(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    num_people = models.IntegerField(editable=False)
    num_days = models.IntegerField(editable=False)
    budget = models.DecimalField(max_digits=10, decimal_places=4, editable=True)

#basket that was recommended to our user by our algorithm
class UserRecommendedBasket(models.Model):
    user = models.OneToOneField(User, primary_key=True)


#basket that was finally transferred to the supermarket (before items failed being transferred etc)
class UserGeneratedBasket(models.Model):
    user = models.OneToOneField(User, primary_key=True)


class UserProductSlack(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    ingredient = models.ForeignKey(AbstractProduct, default=-1, editable=False)
    product = models.ForeignKey(Product, default=-1, editable=False)
    slack = models.DecimalField(max_digits=10, decimal_places=4, editable=True)
    purchase_time = models.DateField(default=0, editable=True)

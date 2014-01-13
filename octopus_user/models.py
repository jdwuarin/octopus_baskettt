from django.db import models
from django.contrib.auth.models import User
from octopus_groceries.models import Product, AbstractProduct


class UserProductSlack(models.Model):

    user = models.ForeignKey(User, default=-1, editable = False)
    ingredient = models.ForeignKey(AbstractProduct, default=-1, editable=False)
    product = models.ForeignKey(Product, default = -1, editable = False)
    slack = models.DecimalField(max_digits = 10, decimal_places = 4, editable = True)
    purchase_time = models.DateField(default= 0, editable = True)

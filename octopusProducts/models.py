from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Product(models.Model):

    #added price, productOrigin, image etc
    price                   = models.CharField(max_length=12, default='NaN', editable=False)
    price_per_unit          = models.CharField(max_length=50, default='NaN', editable=False)
    product_origin           = models.CharField(max_length=50, default='none', editable=False)
    #max_length is defaulted to 100 for image.
    external_image_link     = models.ImageField(upload_to="images/" + str(product_origin) + "/", default='', editable=False)
    name                    = models.CharField(max_length=150, default='', editable=False)
    link                    = models.CharField(max_length=200, default='', editable=False)
    description             = models.CharField(max_length=300, default='')
    offer_flag              = models.CharField(max_length=12, default=False, editable=False)
    external_id             = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.price) + ", " + str(self.product_origin)





class Recipe(models.Model):

    #max_length is defaulted to 100 for image.

    name            = models.CharField(max_length=150, default='', editable=False)
    rating          = models.DecimalField(max_digits=5, decimal_places=4, editable=False)
    review_count    = models.IntegerField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.rating)






class Ingredient(models.Model):

    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name)





class Recipe_ingredient(models.Model):

    recipe      = models.ForeignKey(Recipe, default=-1, editable=False)
    ingredient   = models.ForeignKey(Ingredient, default=-1, editable=False)
    quantity        = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.recipe_id) + ", " + str(self.ingredient_id) + ", " + str(self.quantity)





class Ingredient_product(models.Model):

    ingredient   = models.ForeignKey(Ingredient, default=-1, editable=False)
    product      = models.ForeignKey(Product, default=-1, editable=False)
    rank            = models.IntegerField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.ingredient_id) + ", " + str(self.product_id) + ", " + str(self.rank)


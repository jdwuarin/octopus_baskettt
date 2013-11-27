from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Product(models.Model):

    #added price, productOrigin, image etc
    price           = models.CharField(max_length=12, default='NaN', editable=False)
    productOrigin   = models.CharField(max_length=50, default='none', editable=False)
    #max_length is defaulted to 100 for image.
    image           = models.ImageField(upload_to="images/" + str(productOrigin) + "/", default='', editable=False)
    name            = models.CharField(max_length=150, default='', editable=False)
    link            = models.CharField(max_length=200, default='', editable=False)
    description     = models.CharField(max_length=300, default='')
    offer_flag      = models.CharField(max_length=12, default=False, editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.price) + ", " + str(self.productOrigin)


class Recipe(models.Model):

    #max_length is defaulted to 100 for image.

    name            = models.CharField(max_length=150, default='', editable=False)
    rating          = models.DecimalField(max_digits=5, decimal_places=4, editable=False)
    review_count    = models.IntegerField(editable=False)
    ingredient_list = models.CharField(max_length=10000)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.rating)



class Ingredient(models.Model):

    name = models.CharField(max_length=150, default='', editable=False)

    #this as to be a list of strings
    def add_ingredients(self, ingredient_list):
        for ingredient_name in ingredient_list:
            try:
                Ingredient.objects.get(name=ingredient_name)
            except ObjectDoesNotExist:
                ingredient = Ingredient()
                ingredient["name"] = ingredient_name
                ingredient.save()

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name)


class RecipeIngredient(models.Model):

    recipe_id       = models.ForeignKey(Recipe)
    ingredient_id   = models.ForeignKey(Ingredient)
    quantity        = models.IntegerField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.recipe_id) + ", " + str(self.ingredient_id) + ", " + str(self.quantity)


class IngredientProduct(models.Model):

    ingredient_id   = models.ForeignKey(Ingredient)
    product_id      = models.ForeignKey(Product)
    rank            = models.IntegerField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.ingredient_id) + ", " + str(self.product_id) + ", " + str(self.rank)


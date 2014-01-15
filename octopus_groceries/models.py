from django.db import models


class Supermarket(models.Model):
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class Product(models.Model):
    #added price, productOrigin, image etc
    price = models.CharField(max_length=12, default='NaN', editable=False)
    quantity = models.CharField(max_length=50, default='NaN', editable=False)
    product_life_expectancy = models.IntegerField(default=-1, editable=False)
    unit = models.CharField(max_length=50, default='none', editable=False)
    supermarket = models.ForeignKey(Supermarket, default=-1, editable=False)
    #max_length is defaulted to 100 for image.
    external_image_link = models.ImageField(upload_to="images/" + str(supermarket) + "/", default='', editable=False)
    name = models.CharField(max_length=150, default='', editable=False)
    link = models.CharField(max_length=200, default='', editable=False)
    description = models.CharField(max_length=300, default='')
    offer_flag = models.CharField(max_length=12, default=False, editable=False)
    external_id = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name) + ", " + \
               str(self.link) + ", " + \
               str(self.price) + ", " + \
               str(self.supermarket) + ", " +\
               str(self.quantity) + ", " + \
               str(self.unit)


class Tag(models.Model):
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class Recipe(models.Model):
    #max_length is defaulted to 100 for image.

    name = models.CharField(max_length=150, default='', editable=False)
    rating = models.DecimalField(max_digits=10, decimal_places=4, editable=False)
    review_count = models.IntegerField(editable=False)

    def __unicode__(self):
        return str(self.name) + ", " + str(self.review_count) + ", " + str(self.rating)


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, default=-1, editable=False)
    recipe = models.ForeignKey(Recipe, default=-1, editable=False)

    def __unicode__(self):
        return str(self.recipe_id) + ", " + str(self.tag_id)


class AbstractProduct(models.Model):
    name = models.CharField(max_length=150, default='', editable=False)
    is_food = models.NullBooleanField(editable=False)
    is_condiment = models.NullBooleanField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.is_food) + ", " + str(self.is_condiment)


class RecipeAbstractProduct(models.Model):
    recipe = models.ForeignKey(Recipe, default=-1, editable=False)
    abstract_product = models.ForeignKey(AbstractProduct, default=-1, editable=False)
    quantity = models.CharField(max_length=150, default='', editable=False)
    unit = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.recipe_id) + ", " + str(self.abstract_product_id) + ", " + str(self.quantity) + ", " + str(
            self.unit)


class AbstractProductProduct(models.Model):
    abstract_product = models.ForeignKey(AbstractProduct, default=-1, editable=False)
    rank = models.IntegerField(editable=False)
    product_tesco = models.ForeignKey(Product, related_name='product_tesco_id', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.abstract_product_id) + ", " + str(self.rank) + ", " + str(self.product_tesco_id)
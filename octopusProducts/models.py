from django.db import models

class Product(models.Model):

    #added price, productOrigin, image etc
    price                   = models.CharField(max_length=12, default='NaN', editable=False)
    quantity                = models.CharField(max_length=50, default='NaN', editable=False)
    unit                    = models.CharField(max_length=50, default='none', editable=False)
    product_origin          = models.CharField(max_length=50, default='none', editable=False)
    #max_length is defaulted to 100 for image.
    external_image_link     = models.ImageField(upload_to="images/" + str(product_origin) + "/", default='', editable=False)
    name                    = models.CharField(max_length=150, default='', editable=False)
    link                    = models.CharField(max_length=200, default='', editable=False)
    description             = models.CharField(max_length=300, default='')
    offer_flag              = models.CharField(max_length=12, default=False, editable=False)
    external_id             = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.price) + ", " + str(self.product_origin) + ", " + str(self.quantity) + ", " + str(self.unit)

class Tag(models.Model):

    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name)

class Recipe(models.Model):

    #max_length is defaulted to 100 for image.

    name            = models.CharField(max_length=150, default='', editable=False)
    rating          = models.DecimalField(max_digits=10, decimal_places=4, editable=False)
    review_count    = models.IntegerField(editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.review_count) + ", " + str(self.rating)


class Tag_recipe(models.Model):

    tag          = models.ForeignKey(Tag, default=-1, editable=False)
    recipe       = models.ForeignKey(Recipe, default=-1, editable=False) 

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.recipe_id) + ", " + str(self.tag_id)


class Ingredient(models.Model):

    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name)


class Recipe_ingredient(models.Model):

    recipe       = models.ForeignKey(Recipe, default=-1, editable=False)
    ingredient   = models.ForeignKey(Ingredient, default=-1, editable=False)
    quantity     = models.CharField(max_length=150, default='', editable=False)
    unit         = models.CharField(max_length=150, default='', editable=False)          

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.recipe_id) + ", " + str(self.ingredient_id) + ", " + str(self.quantity) + ", " + str(self.unit)


class Ingredient_product(models.Model):

    ingredient          = models.ForeignKey(Ingredient, default=-1, editable=False)
    rank                = models.IntegerField(editable=False)
    product_tesco       = models.ForeignKey(Product, related_name='product_tesco_id', editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.ingredient_id) + ", " + str(self.rank) + ", " + str(self.product_tesco_id) 


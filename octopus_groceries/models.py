from django.db import models
from django_hstore import hstore


class Supermarket(models.Model):
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class Department(models.Model):
    name = models.CharField(max_length=300, default='', editable=False)
    # matches supermarket_ids to names used in that particular supermarket
    # for the matching department (same goes for aisles and categories)
    supermarket_names = hstore.DictionaryField()

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.name)


class Aisle(models.Model):  # one level bellow Department
    name = models.CharField(max_length=300, default='', editable=False)
    department = models.ForeignKey(Department,
        default=None, blank=True, null=True, editable=False)
    supermarket_names = hstore.DictionaryField()

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.name)


class Category(models.Model):  # one level bellow Aisle
    name = models.CharField(max_length=300, default='', editable=False)
    department = models.ForeignKey(Department,
        default=None, blank=True, null=True, editable=False)
    aisle = models.ForeignKey(Aisle,
        default=None, blank=True, null=True, editable=False)
    supermarket_names = hstore.DictionaryField()

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.name)


class Product(models.Model):
    supermarket = models.ForeignKey(
        Supermarket, default=None, blank=True, null=True, editable=False)
    department = models.ForeignKey(
        Department, default=None, blank=True, null=True, editable=False)
    aisle = models.ForeignKey(
        Aisle, default=None, blank=True, null=True, editable=False)
    category = models.ForeignKey(
        Category, default=None, blank=True, null=True, editable=False)

    #added price, productOrigin, image etc
    price = models.CharField(max_length=12, default='NaN', editable=False)
    quantity = models.CharField(max_length=50, default='NaN', editable=False)
    product_life_expectancy = models.IntegerField(default=-1, editable=False)
    unit = models.CharField(max_length=50, default='none', editable=False)
    #max_length is defaulted to 100 for image.
    external_image_link = models.ImageField(
        max_length=200,upload_to="images/" + str(
            supermarket.name) + "/", default='', editable=False)
    name = models.CharField(max_length=150, default='', editable=False)
    link = models.CharField(max_length=200, default='', editable=False)
    description = models.CharField(max_length=300, default='')
    promotion_flag = models.NullBooleanField(editable=False)
    promotion_description = models.CharField(max_length=200, default="")
    external_id = models.CharField(max_length=150, default='', editable=False)
    ingredients = models.TextField(default='', editable=True)
    in_stock = models.NullBooleanField(editable=False)  # is product available

    def __unicode__(self):
        return str(self.name) + ", " + str(
            self.link) + ", " + str(
            self.price) + ", " + str(
            self.supermarket) + ", " + str(
            self.quantity) + ", " + str(
            self.unit)


class NutritionalFacts(models.Model):
    product = models.OneToOneField(Product, primary_key=True)

    energy = models.DecimalField(max_digits=10, decimal_places=4,
                                 editable=False)
    protein = models.DecimalField(max_digits=10, decimal_places=4,
                                  editable=False)
    carbohydrates = models.DecimalField(max_digits=10, decimal_places=4,
                                        editable=False)
    sugar = models.DecimalField(max_digits=10, decimal_places=4,
                                editable=False)
    starch = models.DecimalField(max_digits=10, decimal_places=4,
                                 editable=False)
    fat = models.DecimalField(max_digits=10, decimal_places=4,
                              editable=False)
    saturates = models.DecimalField(max_digits=10, decimal_places=4,
                                    editable=False)
    monounsaturates = models.DecimalField(max_digits=10, decimal_places=4,
                                          editable=False)
    polyunsaturates = models.DecimalField(max_digits=10, decimal_places=4,
                                          editable=False)
    fibre = models.DecimalField(max_digits=10, decimal_places=4,
                                editable=False)
    salt = models.DecimalField(max_digits=10, decimal_places=4,
                               editable=False)
    sodium = models.DecimalField(max_digits=10, decimal_places=4,
                                 editable=False)


class Tag(models.Model):  # for recipes
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class Recipe(models.Model):
    #max_length is defaulted to 100 for image.

    name = models.CharField(max_length=150, default='', editable=False)
    rating = models.DecimalField(max_digits=10, decimal_places=4,
                                 editable=False)
    review_count = models.IntegerField(editable=False)

    def __unicode__(self):
        return str(self.name) + ", " + str(
            self.review_count) + ", " + str(
            self.rating)


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, default='', editable=False)
    recipe = models.ForeignKey(Recipe, default='', editable=False)

    def __unicode__(self):
        return str(self.recipe_id) + ", " + str(self.tag_id)


class AbstractProduct(models.Model):
    name = models.CharField(max_length=150, default='', editable=False)
    is_food = models.NullBooleanField(editable=False)
    is_condiment = models.NullBooleanField(editable=False)

    def __unicode__(
            self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(
            self.is_food) + ", " + str(
            self.is_condiment)


class RecipeAbstractProduct(models.Model):
    recipe = models.ForeignKey(Recipe, default='', editable=False)
    abstract_product = models.ForeignKey(AbstractProduct, default='',
                                         editable=False)
    quantity = models.CharField(max_length=150, default='', editable=False)
    unit = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.recipe_id) + ", " + str(
            self.abstract_product_id) + ", " + str(
            self.quantity) + ", " + str(
            self.unit)


#maps AbstractProducts to Supermarket specific products
class AbstractProductSupermarketProduct(models.Model):
    abstract_product = models.ForeignKey(AbstractProduct, default='',
                                         editable=False)
    supermarket = models.ForeignKey(Supermarket, default='', editable=False)
    product_dict = hstore.ReferencesField()

    objects = hstore.HStoreManager()

    def __unicode__(
            self):  # just adding this method to say what to display when asked in shell
        return str(self.abstract_product_id) + ", " + str(
            self.rank) + ", " + str(
            self.product)
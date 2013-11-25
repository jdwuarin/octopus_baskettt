# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from octopusProducts.models import Product, Recipe

class ProductItem(DjangoItem):
    django_model = Product

class RecipeItem(DjangoItem):
    django_model = Recipe

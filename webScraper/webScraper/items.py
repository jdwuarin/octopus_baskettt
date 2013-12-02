# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from octopusProducts.models import Product, Recipe


class Product_item(DjangoItem):
    django_model = Product
    matching_ingredient = Field()
    rank = Field()

class Recipe_item(DjangoItem):
    django_model = Recipe
    ingredient_list = Field()
    quantity_list = Field()

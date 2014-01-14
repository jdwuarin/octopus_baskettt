# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from octopus_groceries.models import Product, Recipe, AbstractProduct, Supermarket


class ProductItem(DjangoItem):
    django_model = Product
    matching_abstract_product = Field()
    rank = Field()


class RecipeItem(DjangoItem):
    django_model = Recipe
    tags = Field()
    abstract_product_items = Field() #name, quantity, unit


class AbstractProductItem(DjangoItem):
    django_model = AbstractProduct()
    quantity = Field()
    unit = Field()


class TescoBasketPortingItem(Item):
    success = Field()
    link = Field()

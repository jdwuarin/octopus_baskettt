# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.core.exceptions import ObjectDoesNotExist
from scrapy.exceptions import DropItem
from octopus_groceries.models import *
from django.db.models import Q
from webScraper.spiders.initial_ingredients import determine_if_condiment
import datetime

import re

class WebscraperPipeline(object):

    def process_item(self, item, spider):
        return item

class TescoPostgresPipeline(object):

    def process_item(self, item, spider):

        if spider.name is "tesco":
            item2 = Product()
            item2 = item.save(commit=False) #not saving to db yet
            try:
                found_item = Product.objects.get(
                    supermarket_id=item['supermarket'],
                    external_id=item['external_id'])
                #only update prices and offer flag if item already exists

                found_item.department = item['department']
                found_item.aisle = item['aisle']
                found_item.category = item['category']
                found_item.price = item['price']
                found_item.quantity = item['quantity']
                found_item.unit = item['unit']
                found_item.external_image_link = item['external_image_link']
                found_item.name = item['name']
                found_item.link = item['link']
                found_item.promotion_flag = item['promotion_flag']
                found_item.promotion_description = item['promotion_description']
                found_item.in_stock = True  # suposedly...
                try:
                    found_item.ingredients = item['ingredients']
                except KeyError:
                    pass  # there were no ingredients for the product
                try:
                    found_item.nutritionalfacts = item['nutritionalfacts']
                except KeyError:
                    pass  # there were no nutrional facts. just pass

                found_item.save()

            except ObjectDoesNotExist:
                #if item does not exist, add it to the db
                item.save()

        return item


class FoodComPostgresPipeline(object):

    def process_item(self, item, spider):

        if spider.name is 'food_com':

            #the recipe object is the object that will be
            #saved to the OctopusProducts_recipe db
            recipe = Recipe()
            recipe = item.save(commit=False)  # just saves the fields contained in the Recipe model
            try:
                pre_existing_item = Recipe.objects.get(name=recipe.name) 
                #recipe already exists (supposedly)
                #don't do anything, all should already be populated
                #let's update the ratings and comment count just in case though
                pre_existing_item.rating = recipe.rating
                pre_existing_item.review_count = recipe.review_count
                pre_existing_item.link = recipe.link
                pre_existing_item.external_image_link = recipe.external_image_link
                pre_existing_item.save()

            except ObjectDoesNotExist:
                #we have to save all the objects in the various dbs.

                recipe.save()
                self.add_abstract_product(item, recipe)
                self.add_tags(item, recipe)

        return item

    @staticmethod
    def add_tags(item, recipe):
        tags = item['tags']

        for tag_string in tags:
            tag = Tag()

            try:
                tag = Tag.objects.get(name=tag_string)
                #if the tag is already in the list, don't add it again
            except ObjectDoesNotExist:
                tag.name = tag_string
                tag.save()

            tag_recipe = TagRecipe(tag=tag, recipe=recipe)
            tag_recipe.save()

    @staticmethod
    def add_abstract_product(item, recipe):

        abstract_product_items = item['abstract_product_items']

        for abstract_product_item in abstract_product_items:

            abstract_product = AbstractProduct()
            name = abstract_product_item['name']
            try:
                quantity = abstract_product_item['quantity']
                unit = abstract_product_item['unit']
            except KeyError:
                continue  # skip abstract_product

            try:
                abstract_product = AbstractProduct.objects.get(name=name)
                #if the abstract_product is already in the list, don't add
                #it again, then update condiment status
                abstract_product.is_condiment = determine_if_condiment(
                    abstract_product).is_condiment

            except ObjectDoesNotExist:
                abstract_product.name = name
                abstract_product.is_food = True  # we know this is scraped form food.com
                abstract_product = determine_if_condiment(abstract_product)
                if not abstract_product is None:
                    abstract_product.save()
                else:
                    continue  # skip abstract_product

            recipe_abstract_product = RecipeAbstractProduct(recipe=recipe,
                abstract_product=abstract_product, quantity=quantity, unit=unit)
            recipe_abstract_product.save()


class AbstractProductProductMatchingPipeline(object):


    banned_deps = None

    @classmethod
    def process_item(cls, item, spider):

        # this is done here because otherwise, calling Department
        # from outside actualy starts the django app and thus the reactor...
        if cls.banned_deps is None:
            cls.banned_deps = Department.objects.filter(Q(name="Baby") |
                                        Q(name="Health & Beauty") |
                                        Q(name="Household") |
                                        Q(name="Pets"))

        if spider.name is "abs_prod_prod_match":

            Apsp = AbstractProductSupermarketProduct

            abstract_product = item['matching_abstract_product']
            matching_product = Product()

            #try seeing if the product actually exists
            try:
                matching_product = Product.objects.get(external_id=item['external_id'],
                                                       supermarket=item['supermarket'])

            except ObjectDoesNotExist:
                # product could not be found, raise exception and continue
                # do not save new item as department etc is not known
                pass

            # try seeing if there already is a matching
            # that corresponds to the product

            apsp, created = Apsp.objects.get_or_create(
                abstract_product=abstract_product,
                supermarket=item['supermarket'])

            # only save the matching product if it is not from one of the banned
            # deps
            if matching_product.department not in cls.banned_deps:
                apsp.product_dict[str(item['rank'])] = matching_product
                apsp.save()
            else:
                # delete if their are no matching products
                if len(apsp.product_dict) == 0:
                    apsp.delete()

        return item


class ProductNotFoundException(Exception):

    def __init__(self, product_id):
        self.value = product_id

    def __str__(self):
        return "could not find " + repr(self.value)
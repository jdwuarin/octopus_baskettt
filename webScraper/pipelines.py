# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.core.exceptions import ObjectDoesNotExist
from scrapy.exceptions import DropItem
from octopus_groceries.models import Product, Recipe, Tag, TagRecipe, \
    RecipeAbstractProduct, AbstractProduct, AbstractProductProduct, Supermarket
from webScraper.spiders.initial_ingredients import determine_if_condiment

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
                supermarket = Supermarket.objects.get(name='tesco')
                pre_existing_item = Product.objects.get(supermarket_id=supermarket,
                    external_id=item2.external_id)
                #only update prices and offer flag if item already exists
                pre_existing_item.price = item2.price
                pre_existing_item.quantity = item2.quantity
                pre_existing_item.unit = item2.unit
                pre_existing_item.offer_flag = item2.offer_flag
                pre_existing_item.save()

            except ObjectDoesNotExist:
                #if item does not exist, add it to the db
                item2.save()

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
                #if the abstract_product is already in the list, don't add
                #it again
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
            recipe_abstract_product = RecipeAbstractProduct()
            name = abstract_product_item['name']
            try:
                quantity = abstract_product_item['quantity']
                unit = abstract_product_item['unit']
            except KeyError:
                continue  # skip abstract_product

            try:
                abstract_product = AbstractProduct.objects.get(name = name)
                #if the abstract_product is already in the list, don't add
                #it again
            except ObjectDoesNotExist:
                abstract_product.name = name
                abstract_product = determine_if_condiment(abstract_product)
                if not abstract_product is None:
                    abstract_product.save()
                else:
                    continue  # skip abstract_product

            recipe_abstract_product = RecipeAbstractProduct(recipe=recipe,
                abstract_product=abstract_product, quantity=quantity, unit=unit)
            recipe_abstract_product.save()


class AbstractProductProductMatchingPipeline(object):

    def process_item(self, item, spider):

        if spider.name is "abs_prod_prod_match":

            abstract_product = item['matching_abstract_product']
            matching_product = Product()

            #try seeing if the product actually exists
            try:
                matching_product = Product.objects.get(external_id=item['external_id'],
                                                       supermarket=item['supermarket'])

            except ObjectDoesNotExist:
                #product could not be found, raise exception and continue
                # raise Product_not_found_exception(item['external_id'])
                matching_product = item.save(commit=False)  # save new item
                matching_product.save()

            #try seeing if there already is a matching that corresponds to the product
            try:
                abstract_product_product = AbstractProductProduct.objects.get(
                    abstract_product=abstract_product,
                    product=matching_product)
                #it already existed with a certain rank, just update said rank
                abstract_product_product.rank = item['rank']
                abstract_product_product.save()
            except ObjectDoesNotExist:
                # matching did not exist yet. remove item with rank of scraped
                try:
                    abstract_product_product_list = AbstractProductProduct.objects.filter(
                        abstract_product=abstract_product,
                        rank=item['rank'])
                    for entry in abstract_product_product_list:
                        if entry.product.supermarket == item['supermarket']:
                            entry.delete()
                except ObjectDoesNotExist:
                    #if there was no such item, do nothing, just add the matching
                    #right after this block
                    pass
                abstract_product_product = AbstractProductProduct(abstract_product=abstract_product,
                                                              rank=item['rank'],
                                                              product = matching_product)
                abstract_product_product.save()


        return item


class ProductNotFoundException(Exception):

    def __init__(self, product_id):
        self.value = product_id

    def __str__(self):
        return "could not find " + repr(self.value)

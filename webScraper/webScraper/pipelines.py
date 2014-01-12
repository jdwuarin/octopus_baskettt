# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.core.exceptions import ObjectDoesNotExist
from scrapy.exceptions import DropItem
from octopus_product.models import Product, Recipe, Tag, Tag_recipe, Recipe_ingredient, Ingredient, Ingredient_product
from webScraper.spiders.initial_ingredients import determine_if_condiment

import re

class WebscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class Tesco_postgres_pipeline(object):
    def process_item(self, item, spider):

        if spider.name is "tesco":
            item2 = Product()
            item2 = item.save(commit=False) #not saving to db yet
            try:
                pre_existing_item = Product.objects.get(product_origin='tesco', 
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


class Food_com_postgres_pipeline(object):

    def process_item(self, item, spider):

        if spider.name is 'food_com':

            #the recipe object is the object that will be
            #saved to the OctopusProducts_recipe db
            recipe = Recipe()
            recipe = item.save(commit=False) #just saves the fields contained in the Recipe model
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
                self.add_ingredients(item, recipe)
                self.add_tags(item, recipe)

        return item

    def add_tags(self, item, recipe):
        tags = item['tags']

        for tag_string in tags:
            tag = Tag()

            try:
                tag = Tag.objects.get(name = tag_string)
                #if the ingredient is already in the list, don't add
                #it again
            except ObjectDoesNotExist:
                tag.name = tag_string
                tag.save()

            tag_recipe = Tag_recipe(tag = tag, recipe = recipe)
            tag_recipe.save()

    def add_ingredients(self, item, recipe):

        ingredient_items = item['ingredient_items']

        for ingredient_item in ingredient_items:

            ingredient = Ingredient()
            recipe_ingredient = Recipe_ingredient()
            name = ingredient_item['name']
            try:
                quantity = ingredient_item['quantity']
                unit = ingredient_item['unit']
            except KeyError:
                continue #skip ingredient

            try:
                ingredient = Ingredient.objects.get(name = name)
                #if the ingredient is already in the list, don't add
                #it again
            except ObjectDoesNotExist:
                ingredient.name = name
                ingredient = determine_if_condiment(ingredient)
                if not ingredient  is None:
                    ingredient.save()
                else:
                    continue #skip ingredient

            recipe_ingredient = Recipe_ingredient(recipe = recipe,
                ingredient = ingredient, quantity = quantity, unit = unit)
            recipe_ingredient.save()




class Ingredient_produt_matching_pipeline(object):

    def process_item(self, item, spider):

        if spider.name is "ing_prod_match":

            ingredient = item['matching_ingredient']
            matching_product = Product()

            try:
                matching_product = Product.objects.get(external_id = item['external_id'], 
                    product_origin = item['product_origin']) 
                    

            except ObjectDoesNotExist:
                #product could not be found, raise exception and continue
                # raise Product_not_found_exception(item['external_id'])
                matching_product = item.save(commit=False) #save new item
                matching_product.save()


            ingredient_product = Ingredient_product(ingredient = ingredient, 
                rank = item['rank'])

            ingredient_product.product_tesco = matching_product

            ingredient_product.save()
        return item


class Product_not_found_exception(Exception):
    def __init__(self, product_id):
        self.value = product_id
    def __str__(self):
        return "could not find " + repr(self.value)

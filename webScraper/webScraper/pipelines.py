# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.core.exceptions import ObjectDoesNotExist
from scrapy.exceptions import DropItem
from octopusProducts.models import Product, Recipe, Recipe_ingredient, Ingredient, Ingredient_product

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
                pre_existing_item.price_per_unit = item2.price_per_unit
                pre_existing_item.offer_flag = item2.offer_flag
                pre_existing_item.save()

            except ObjectDoesNotExist:
                #if item does not exist, add it to the db
                item2.save()


        return item


class All_recipes_postgres_pipeline(object):

    def process_item(self, item, spider):

        if spider.name is "allrecipes":

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

        return item


    def add_ingredients(self, recipe_item, recipe):

        ingredient_list = self.ingredient_list_cleaner(recipe_item['ingredient_list'])
        quantity_list = recipe_item['quantity_list']
        ingredients_data = dict(zip(ingredient_list, quantity_list))

        for ingredient_name, ingredient_quantity in ingredients_data.iteritems():

            ingredient = Ingredient()
            recipe_ingredient = Recipe_ingredient()

            try:
                ingredient = Ingredient.objects.get(name=ingredient_name)
                #if the ingredient is already in the list, don't add
                #it again
            except ObjectDoesNotExist:
                ingredient.name = ingredient_name
                ingredient.save()

            recipe_ingredient = Recipe_ingredient(recipe = recipe,
                ingredient = ingredient, quantity = ingredient_quantity)
            recipe_ingredient.save()

        return


    def ingredient_list_cleaner(self, ingredient_list):

        return_list = []

        for ingredient in ingredient_list:

            #only add ingredients that don't contain non alpha characters
            if ingredient == "" or ingredient == " " or not re.match('^[a-zA-Z ]*$', ingredient):
                continue

            return_list.append(ingredient)

        return return_list


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



class Tesco_basket_porting_pipeline(object):
    def process_item(self, item, spider):

        if spider.name is "tesco_basket":
            if item['success'] is "False":
                raise DropItem("someFailure occures in" % item)
            else:
                return item

        else:
            return item



class Product_not_found_exception(Exception):
    def __init__(self, product_id):
        self.value = product_id
    def __str__(self):
        return "could not find " + repr(self.value)

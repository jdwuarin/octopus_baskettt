import random
from math import floor, ceil
from django.db.models import Q

from octopus_groceries.models import *
from unit_helper import Unit_helper


#per person limit cost for single product
product_cost_limit = 6

class BasketRecommendationEngine(object):
    condiment_max_ratio = 0.2
    num_condiment_abstract_product = 0.0
    num_returned_prod_per_abstract_product = 20

    # In the default product list, no products
    # should stem from any of those departments
    # TODO remove this bad looking hack

    banned_deps = Department.objects.filter(Q(name="Baby") |
                                            Q(name="Health & Beauty") |
                                            Q(name="Household") |
                                            Q(name="Pets"))

    @classmethod
    def create_onboarding_basket(cls, user_settings):
        #TODO, remove tesco hard-code

        tag_list = Tag.objects.filter(name__in=user_settings.tags)

        potential_recipe_list = []
        for tag in tag_list:
            tag_recipe_list = TagRecipe.objects.filter(tag=tag.id)
            recipe_id_list = [tag_recipe.recipe_id for tag_recipe in
                              tag_recipe_list]
            recipe_list = Recipe.objects.filter(id__in=recipe_id_list).order_by(
                '-review_count', '-rating')
            potential_recipe_list.append(recipe_list)

        product_list = []
        if len(potential_recipe_list) > 0:
            product_list = cls.get_product_matrix(potential_recipe_list,
                                                user_settings)
        return product_list

    @classmethod
    def get_product_matrix(cls, potential_recipes, user_settings):
        recipe_type_passed = 0
        meals_per_day = 1  # should probably be in user_settings somehow
        product_matrix = []
        i = 0

        # a rough recipe_list is first gathered
        recipe_list = []
        while len(recipe_list) * meals_per_day < user_settings.days:

            for ii, recipe in enumerate(potential_recipes):

                try:
                    recipe = recipe[i / len(
                        potential_recipes)]  # the division will floor the value, which is what we want
                except IndexError:
                    recipe_type_passed += 1
                    if recipe_type_passed == len(potential_recipes):
                        break_condition = True
                        break
                    else:
                        continue  # if no more recipe of that kind, go to next kind

                recipe_list.append(recipe)

        # mappings to abstract_products are then obtained
        recipe_abstract_product_list = (
            RecipeAbstractProduct.objects.filter(
                recipe__in=recipe_list).order_by('abstract_product'))

        # units are dealt with separating abstract_products in
        # a list requiring grams and "each" of a certain abstract_product.
        # returned dicts are or the form: my_dict[abstract_product] = quantity
        abstract_products_grams, abstract_products_each =\
            Unit_helper.get_abstract_products_by_unit(
                recipe_abstract_product_list)

        # we first filter out the "too many" condiments that we might have
        cls.filter_out_extra_condiments(abstract_products_grams)
        cls.filter_out_extra_condiments(abstract_products_each)

        # we then filter out all the ingredients that do not
        # respects the users diet or banned meats or products etc...
        cls.filter_diet(abstract_products_grams, user_settings)
        cls.filter_diet(abstract_products_each, user_settings)

        cls.filter_banned_meats(abstract_products_grams, user_settings)
        cls.filter_banned_meats(abstract_products_each, user_settings)

        # a product matrix is then obtained for each unit type
        # where the result looks like:
        # product_matrix[0] = [[selected_product, quantity], other_prod1, op2,...]
        product_matrix = cls.get_products_to_buy(
            abstract_products_grams, user_settings, "grams")
        product_matrix += cls.get_products_to_buy(
            abstract_products_each, user_settings, "each")

        # the lists are then merged.
        product_matrix = cls.merge_matrix(product_matrix)

        return product_matrix

    #check that condiment_ratio is not passed
    # first obtain condiment ratio on list
    @classmethod
    def filter_out_extra_condiments(cls, abstract_products):
        condiment_count = 0.0

        if not abstract_products:
            return None

        for abstract_product in abstract_products:
            if abstract_product.is_condiment:
                condiment_count += 1.0

        if condiment_count/float(len(abstract_products)) > (
            cls.condiment_max_ratio):
            # there are too many condiments here, remove a certain amount
            # such that: (condiment_count - num_to_remove)/
            # len(abstract_products - num_to_remove) < 0.3
            num_to_remove = (condiment_count -
                             cls.condiment_max_ratio *
                             float(len(abstract_products))) / (
                        1.0 - cls.condiment_max_ratio)
            num_to_remove = ceil(num_to_remove)

            num_removed = 0
            aptd = []  # abstract_products to delete
            for abstract_product in abstract_products:
                if abstract_product.is_condiment:
                    aptd.append(abstract_product)
                    num_removed += 1
                if num_removed >= num_to_remove:
                    break

            for abstract_product in aptd:
                del abstract_products[abstract_product]

    # TODO, implement these two filters
    @classmethod
    def filter_diet(cls, abstract_products, user_settings):

        pass

    @classmethod
    def filter_banned_meats(cls, abstract_products, user_settings):

        pass

    @classmethod
    def get_products_to_buy(cls,
                            abstract_products,
                            user_settings,
                            abstract_product_unit):

        # product_matrix[0] = [[selected_product, quantity], other_prod1, op2,...]
        product_matrix = []
        for abstract_product, quantity in abstract_products.iteritems():

            # get list of products attached to abstract_product:
            apsp = AbstractProductSupermarketProduct.objects.get(
                abstract_product=abstract_product,
                supermarket=user_settings.default_supermarket)

            my_prod_rank = cls.get_selected_product_rank(
                apsp, user_settings.price_sensitivity)

            if my_prod_rank is None:
                continue  # deal with non existing objects

            product_list = []
            selected_product = apsp.product_dict[str(my_prod_rank)]
            quantity_to_buy = cls.get_quantity_for_product(
                                 selected_product,
                                 user_settings,
                                 abstract_product_unit,
                                 quantity)
            product_list.append([selected_product,
                                 quantity_to_buy])

            # populate with other similar products that can be selected
            for ii in range(1, len(apsp.product_dict)+1):
                if ii != my_prod_rank:
                    product_list.append(
                        apsp.product_dict[str(ii)])

            if product_list:
                product_matrix.append(product_list)

        return product_matrix

    # selects the most appropriate product in a list based
    # solely on price_sensitivity of the user
    # complexity: O(n) in min(num_products and selected_within_rank)
    @classmethod
    def get_selected_product_rank(cls, apsp, price_sensitivity):

        select_within_rank = 5
        num_prod = len(apsp.product_dict)

        if num_prod < 1:
            return None

        loop_size = int(min(num_prod, select_within_rank))

        considered_products = []
        # starting at 1 because ranks start at 1 and not 0
        for ii in range(1, loop_size):
            considered_products.append([apsp.product_dict[str(ii)], ii])

        # just sort with respect to price/quantity
        considered_products = sorted(considered_products,
            key=lambda product:
            float(product[0].price.replace("GBP", ""))/float(
                product[0].quantity))

        # we floor the value because as always, indexes start at 0
        # the floor is done via the int() function
        selected_rank = considered_products[
            int(price_sensitivity * loop_size)][1]

        return selected_rank

    # determines what quantity should be purchased of a certain
    # product based on the basket requirements and the user
    # complexity: tbd
    @classmethod
    def get_quantity_for_product(cls,
                                 product,
                                 user_settings,
                                 abstract_product_unit,
                                 abstract_product_quantity):

        prod_usage = Unit_helper.get_product_usage(abstract_product_unit,
                                                   product.unit,
                                                   abstract_product_quantity)

        quantity_to_buy = ceil((float(
            user_settings.people) * float(
            prod_usage)) / float(
            product.quantity))

        return quantity_to_buy

    @classmethod
    def merge_matrix(cls, product_matrix):

        product_matrix = sorted(product_matrix,
                                key=lambda entry: entry[0][0])

        output_product_matrix = []
        output_product_matrix.append(product_matrix[1])

        loop_range = len(product_matrix)
        for ii in range(1, loop_range):
            # essentially test the last product of the output.
            # if it is the same as the one being iterated over, just
            # add quantities instead of returning multiple products.
            if output_product_matrix[-1][0][0] == product_matrix[ii][0][0]:
                output_product_matrix[-1][0][1] += product_matrix[ii][0][1]
            else:
                output_product_matrix.append(product_matrix[ii])

        return output_product_matrix
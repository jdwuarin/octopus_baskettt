import random
from math import floor, ceil

from octopus_groceries.models import Tag, Recipe, TagRecipe, \
    RecipeAbstractProduct, AbstractProduct, AbstractProductProduct, Product
from unit_helper import Unit_helper


#per person limit cost for single product
product_cost_limit = 6


class BasketRecommendationEngine(object):
    num_days_sigma_acceptance_rate = 0.3
    condiment_max_ratio = 0.3
    num_condiment_abstract_product = 0.0

    #remove this bad looking hack
    banned_word = " Cat"

    @classmethod
    def create_onboarding_basket(cls, basket_onboarding_info):
        #TODO, remove tesco hard-code

        tag_list = Tag.objects.filter(name__in=basket_onboarding_info.tags)

        potential_recipe_list = []
        for tag in tag_list:
            tag_recipe_list = TagRecipe.objects.filter(tag=tag.id)
            recipe_id_list = [tag_recipe.recipe_id for tag_recipe in tag_recipe_list]
            recipe_list = Recipe.objects.filter(id__in=recipe_id_list).order_by('-review_count', '-rating')
            potential_recipe_list.append(recipe_list)

        product_list = {}
        if len(potential_recipe_list) > 0:
            product_list = cls.get_product_list(potential_recipe_list, basket_onboarding_info.budget,
                                                basket_onboarding_info.people)

        return product_list

    @classmethod
    def get_product_list(cls, recipes, budget, people):
        recipe_type_passed = 0
        break_condition = False
        basket_cost = 0
        #abstract_product, [selected_product, slack(remaining for use for other recipes)]
        product_list_slack = {}
        #product, [quantity_to_buy, mapped abstract_product]
        product_list = {}
        i = 0

        while basket_cost < budget:

            for __, recipe in enumerate(recipes):
            # for x in range(0, len(recipes)):
                try:
                    recipe = recipe[i / len(recipes)]  # the division will floor the value, which is what we want
                except IndexError:
                    recipe_type_passed += 1
                    if recipe_type_passed == len(recipes):
                        break_condition = True
                        break
                    else:
                        continue  # if no more recipe of that kind, go to next kind

                recipe_abstract_product_list = RecipeAbstractProduct.objects.filter(recipe=recipe)
                should_break, added_cost = cls.merge_lists(recipe_abstract_product_list, product_list_slack,
                                                           product_list, people, int(budget) - basket_cost)

                basket_cost += added_cost
                if should_break:
                    break_condition = True
                    break

                i += 1

            if break_condition:
                break

        return product_list

    @classmethod
    def merge_lists(cls, recipe_abstract_product_list, product_list_slack,
                    product_list, people, recipe_allowance):

        recipe_allowance_start = recipe_allowance
        should_break = False
        for recipe_abstract_product in recipe_abstract_product_list:
            abstract_product = AbstractProduct.objects.get(id=recipe_abstract_product.abstract_product.id)
            qu_ing_needed = None
            #first try seeing if I still have some slack of the required
            #abstract_product in my basket
            try:
                selected_product, slack = product_list_slack[abstract_product]

                #same values in the two different units
                prod_usage = Unit_helper.get_product_usage(
                    recipe_abstract_product, selected_product)
                if prod_usage == "-1":
                    continue  # there was an error, skip abstract_product

                remaining_slack = slack - (float(people) * float(prod_usage))

                if remaining_slack >= 0:
                    #just reduce slack, don't add any product to basket though
                    product_list_slack[abstract_product] = (selected_product, remaining_slack)
                    continue
                else:
                    #quantity of abstract_product still needed
                    del product_list_slack[abstract_product]
                    qu_ing_needed = (-float(remaining_slack) / (
                        float(people) * float(prod_usage))) * float(recipe_abstract_product.quantity)

            except KeyError:
                pass

            #abstract_product not yet in the basket.
            #find suitable product and add it to
            #basket in a minimum of required quantity
            potential_product_list = AbstractProductProduct.objects.filter(
                abstract_product_id=abstract_product.id).order_by("rank")
            if len(potential_product_list) == 0:
                continue  # deal with items not found in db

            potential_product_index_to_get = int(floor(min(len(potential_product_list), 3) * random.random()))
            # TODO this is to condition for other supermarkets to work too
            selected_product = Product.objects.get(
                id=potential_product_list[potential_product_index_to_get].product_tesco_id)

            prod_usage = Unit_helper.get_product_usage(recipe_abstract_product, selected_product, qu_ing_needed)

            quantity_to_buy = ceil((float(people) * float(prod_usage)) / float(selected_product.quantity))
            slack = quantity_to_buy * float(selected_product.quantity) - (float(people) * float(prod_usage))

            product_cost = quantity_to_buy * float(selected_product.price.replace("GBP", ""))

            if people * product_cost_limit < product_cost or cls.banned_word in selected_product.name:
                continue  # don't add items that are deemed too expensive or contained a banned word

            #check that condiment_ratio is not passed
            if abstract_product.is_condiment:
                if len(product_list) > 0 and (
                        cls.num_condiment_abstract_product / len(product_list) > cls.condiment_max_ratio):
                    continue  # don't add extra condiment to basket
                else:
                    cls.num_condiment_abstract_product += 1.0

            #check that cost is not passed
            recipe_allowance -= quantity_to_buy * float(selected_product.price.replace("GBP", ""))

            if recipe_allowance < 0:
                should_break = True
                break

            product_list_slack[abstract_product] = (selected_product, slack)

            try:
                bought_quantity = product_list[selected_product][0]  # change that
                product_list[selected_product] = [bought_quantity + quantity_to_buy, abstract_product]

            except KeyError:
            # product was not yet in basket
                product_list[selected_product] = [quantity_to_buy, abstract_product]

        return should_break, recipe_allowance_start - recipe_allowance
from octopusProducts.models import Tag, Recipe, Tag_recipe, Recipe_ingredient, Ingredient, Ingredient_product, Product
from unit_helper import Unit_helper
import random
from math import floor, ceil

#per person limit cost for single product
product_cost_limit = 5

class Basket_recommendation_engine(object):

	num_days_sigma_acceptance_rate = 0.3

	@classmethod
	def create_onboarding_basket(cls, basket_onboarding_info):
		#TODO, remove tesco hardcode 

		tag_list = Tag.objects.filter(name__in = basket_onboarding_info.tags)

		potential_recipe_list = []
		for tag in tag_list:

			tag_recipe_list = Tag_recipe.objects.filter(tag = tag.id)
			recipe_id_list = [tag_recipe.recipe_id for tag_recipe in tag_recipe_list]
			recipe_list = Recipe.objects.filter(id__in = recipe_id_list).order_by('-review_count', '-rating')
			potential_recipe_list.append(recipe_list)

		product_list = cls.get_product_list(potential_recipe_list, basket_onboarding_info.budget,
			basket_onboarding_info.people)
		return product_list

	@classmethod
	def get_product_list(cls, recipes, budget, people):
		recipe_type_passed = 0
		break_condition = False
		basket_cost = 0
		#ingredient, [selected_product, slack(remaining for use for other recipes)]
		product_list_slack = {}
		#product, [quantity_to_buy, mapped recipe_ingredient]
		product_list = {}
		i=0
		while basket_cost < budget:

			for x in range(0, len(recipes)):

				try:
					recipe = recipes[x][i / len(recipes)] #the division will floor the value, which is what we want
				except IndexError:
					recipe_type_passed = recipe_type_passed + 1
					if recipe_type_passed == len(recipes):
						break_condition = True
						break
					else:
						continue #if no more recipe of that kind, go to next kind

				recipe_ingredients_list = Recipe_ingredient.objects.filter(recipe = recipe)
				should_break, added_cost = cls.merge_lists(recipe_ingredients_list, product_list_slack, 
					product_list, people, budget - basket_cost)

				basket_cost += added_cost
				if should_break:
					break_condition = True
					break

				i = i + 1

			if break_condition:
				break

		return product_list

	@classmethod
	def merge_lists(cls, recipe_ingredient_list, product_list_slack, 
		product_list, people, recipe_allowance):

		recipe_allowance_start = recipe_allowance
		should_break = False
		for recipe_ingredient in recipe_ingredient_list:
			ingredient = Ingredient.objects.get(id = recipe_ingredient.ingredient.id)
			qu_ing_needed = None
			#first try seeing if I still have some slack of the required
			#ingredient in my basket
			try: 
				selected_product, slack = product_list_slack[ingredient]

				#same values in the two different units
				prod_usage = Unit_helper.get_product_usage(
					recipe_ingredient, selected_product)
				if prod_usage == "-1":
					continue #there was an error, skip ingredient

				remaining_slack = slack - (float(people) * float(prod_usage))


				if remaining_slack >= 0:
					#just reduce slack, don't add any product to basket though
					product_list_slack[ingredient] = (selected_product, remaining_slack)
					continue
				else:
					#quantity of ingredient still needed
					del product_list_slack[ingredient]
					qu_ing_needed = (-float(remaining_slack)/(
						float(people) * float(prod_usage))) * float(recipe_ingredient.quantity)

			except KeyError:
				pass

			#ingredient not yet in the basket.
			#find suitable product and add it to 
			#basket in a minimum of required quantity
			potential_product_list = Ingredient_product.objects.filter(
				ingredient_id = ingredient.id).order_by("rank")
			if len(potential_product_list) == 0:
				continue #deal with items not found in db

			potential_product_index_to_get = int(floor(min(len(potential_product_list), 1) * random.random()))
			selected_product = Product.objects.get(
					id = potential_product_list[potential_product_index_to_get].product_tesco_id)

			prod_usage = Unit_helper.get_product_usage(recipe_ingredient, selected_product, qu_ing_needed)



			quantity_to_buy = ceil((float(people) * float(prod_usage)) / float(selected_product.quantity))
			slack = quantity_to_buy * float(selected_product.quantity) - (float(people) * float(prod_usage))

			product_cost = quantity_to_buy * float(selected_product.price.replace("GBP", ""))
			if people * product_cost_limit < product_cost:
				continue #don't add items that are deemed to expensive

			#check that cost is not passed
			recipe_allowance = recipe_allowance - quantity_to_buy * float(selected_product.price.replace("GBP", ""))

			if recipe_allowance < 0:
				should_break = True
				break

			product_list_slack[ingredient] = (selected_product, slack)

			try:
				dummy, bought_quantity = product_list[selected_product]#change that
				product_list[selected_product] = [recipe_ingredient, bought_quantity + quantity_to_buy]

			except KeyError:
			# product_list[selected_product] = quantity_to_buy
				product_list[selected_product] = [recipe_ingredient, quantity_to_buy]

				#TODO get rid of water ingredient and do some other hard_coding stuff

			# product_list.append([selected_product, recipe_ingredient, quantity_to_buy])

		return should_break, recipe_allowance_start - recipe_allowance


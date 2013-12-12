from octopusProducts.models import Cuisine, Recipe

class Basket_recommendation_engine():

	@classmethod
	def create_onboarding_basket(cls, basket_onboarding_info):
		#TODO, remove tesco hardcode 

		recipe_average_price = 7.0
		potential_num_recipes = int((basket_onboarding_info.budget * 3.0) / recipe_average_price)

		cuisine_id_list = []
		for cuisine in basket_onboarding_info.cuisines:
			cuisine_id_list.append(Cuisine.objects.get(name = cuisine)[0].id)

		potential_num_recipes_by_cuisine = potential_num_recipes / len(cuisine_id_list)

		potential_recipe_list = []
		for cuisine_id in cuisine_id_list:
			recipe_list_by_cuisine = Recipe.objects.filter(cuisine_id = cuisine_id, 
			course__in = ["Main Dishes", "Lunch"]).order_by('review_count', 'rating')[:potential_num_recipes_by_cuisine] 
			potential_recipe_list.append(recipe_list_by_cuisine)


		# pre_selected_recipes = []
		# for cuisine_id in potential_recipe_list:
		# 	for x in range(0, potential_num_recipes):
		# 		pre_selected_recipes.append(potential_recipe_list[cuisine_id][x])


		final_recipe_list = cls.filter_recipes_by_budget(potential_recipe_list, basket_onboarding_info.budget)

	@classmethod
	def filter_recipes_by_budget(cls, recipes, budget):
		break_condition = False
		basket_cost = 0
		final_basket = []
		i=0
		while basket_cost < budget:

			for cuisine_id in recipes:
				recipe = recipes[cuisine_id][i % len(recipes)]
				basket_cost = recipe.get_cost()
				if basket_cost > budget:
					break_condition = True
					break
				final_basket.append(recipe)

			if break_condition:
				break







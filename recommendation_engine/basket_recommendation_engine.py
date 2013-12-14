from octopusProducts.models import Tag, Recipe, Tag_recipe

class Basket_recommendation_engine():

	@classmethod
	def create_onboarding_basket(cls, basket_onboarding_info):
		#TODO, remove tesco hardcode 

		recipe_average_price = 7.0
		potential_num_recipes = int((basket_onboarding_info.budget * 9.0) / recipe_average_price)

		tag_list = Tag.objects.filter(name__in = basket_onboarding_info.tags)

		potential_num_recipes_by_tag = potential_num_recipes / len(tag_list)

		potential_recipe_list = []
		for tag in tag_list:

			tag_recipe_list = Tag_recipe.objects.filter(tag = tag.id)
			recipe_id_list = [tag_recipe.recipe_id for tag_recipe in tag_recipe_list]
			recipe_list = Recipe.objects.filter(id__in = recipe_id_list).order_by('-review_count', '-rating')[:potential_num_recipes_by_tag]
			# course__in = ["Main Dishes", "Lunch"])
			potential_recipe_list.append(recipe_list)

		final_recipe_list = cls.filter_recipes_by_budget(potential_recipe_list, basket_onboarding_info.budget)
		product_list = cls.get_produt_list(final_recipe_list)
		print product_list

	@classmethod
	def filter_recipes_by_budget(cls, recipes, budget):
		break_condition = False
		basket_cost = 0
		final_basket = []
		i=0
		while basket_cost < budget:

			for x in range(0, len(recipes)): 
				recipe = recipes[x][i / len(recipes)] #the division will floor the value, which is what we want
				# basket_cost = recipe.get_cost()
				basket_cost = basket_cost + 7
				if basket_cost > budget:
					break_condition = True
					break
				i = i + 1
				final_basket.append(recipe)

			if break_condition:
				break

		return final_basket

	@classmethod
	def get_product_list(cls, recipe_list):
		pass







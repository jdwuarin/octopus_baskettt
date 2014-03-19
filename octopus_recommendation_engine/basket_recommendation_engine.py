from octopus_user.models import UserRecommendedBasket, UserSettings
from octopus_groceries.models import *
import octopus_user
import helpers
import onboarding_basket_helpers
import later_basket_helpers


def create_onboarding_basket(user, data=None):

    print data
    user_settings = helpers.get_user_settings_from_user(user, data)

    # get the tags id list from the user settings
    tags_id = octopus_user.helpers.get_list_from_comma_separated_string(
        user_settings.tags)

    pre_tag_list = Tag.objects.filter(id__in=tags_id)

    #this is a hot fix for the fact that
    #the only tag for european type cuisines that exists is "European"
    tag_list = []
    for tag in pre_tag_list:
        # id's 1 and 2 contain the Italian and French tags
        # as per specified in the tag_fixtures.json file
        if tag.id == 1 or tag.id == 2:
            tag_list.append(Tag.objects.get(name="European"))
        else:
            tag_list.append(tag)

    potential_recipe_list = []
    for tag in tag_list:
        tag_recipe_list = TagRecipe.objects.filter(tag=tag.id)
        recipe_id_list = [tag_recipe.recipe_id for tag_recipe in
                          tag_recipe_list]
        recipe_list = Recipe.objects.filter(id__in=recipe_id_list).order_by(
            '-review_count', '-rating')
        potential_recipe_list.append(recipe_list)

    product_matrix = []
    if len(potential_recipe_list) > 0:
        product_matrix = onboarding_basket_helpers.get_product_matrix(
            potential_recipe_list,
            user_settings)

    basket = helpers.get_json_basket(product_matrix)
    return basket, user_settings


def get_or_create_later_basket(user):

    # see if user has some baskets
    ugb = octopus_user.models.UserGeneratedBasket.objects.filter(
        user=user).order_by('-time')
    urb = octopus_user.models.UserRecommendedBasket.objects.filter(
        user=user).order_by('-time')

     # no basket generated by user yet, just create an anonymous one.
    if not ugb:
        basket, __ = create_onboarding_basket(user)
        #save it as a UserRecommendedBasket
        user_recommended_basket = (
            helpers.create_user_recommended_basket_from_basket(basket, user))
        user_recommended_basket.save()
        urb_id = user_recommended_basket.id
        return basket, urb_id


    # user has edited at least one basket

    # see when the last recommended basket was created compared
    # to the last generated basket
    last_urb = urb[len(urb)-1]
    last_ugb = ugb[len(ugb)-1]
    last_urb_created_after_last_ugb = last_urb > last_ugb

    if last_urb_created_after_last_ugb:
        basket = helpers.get_basket_from_user_recommended_basket(last_urb)
        return basket, last_urb.id


    #TODO actually write this algorithm or more hopefully a slightly better one in later_basket_helpers.
    # if need for new recommendation,
    # take last and just remove 20% switching them with similar
    # in similar aisle (yes, this is sort of a shitty hack)
    basket = []
    #recommended_basket product_dict
    rb_product_dict = {}
    for id, quantity in last_ugb.product_dict.iteritems():
        try:
            rb_product_dict[str(id)] = str(quantity)
            product = Product.objects.get(id=id)
            basket.append([[product, quantity]])
        except Product.DoesNotExist:
            pass

    # save the recommended basket
    urb = UserRecommendedBasket(user=user,
                              product_dict=rb_product_dict)
    urb.save()

    basket = helpers.get_json_basket(basket)
    return basket, urb.id
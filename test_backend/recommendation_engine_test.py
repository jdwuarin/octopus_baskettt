from octopus_recommendation_engine.basket_onboarding_info import BasketOnboardingInfo
from octopus_recommendation_engine.basket_recommendation_engine import BasketRecommendationEngine
from octopus_groceries.models import Tag, Recipe, TagRecipe, Supermarket
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.http import HttpResponse
import json


def basket_porting_test(request, basket_before):

    SpiderManagerController.create_if_none()

    # for testing purposes
    email = "arnaudbenard13+test@gmail.com"
    password = "test123"

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               basket_before, thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    basket_after = this_basket.thread_manager.get_response()
    basket_after = check_basket_persistence(basket_before, basket_after)

    #####################
    for key, value in basket_after.iteritems():
        print key, value
    #####################

    return HttpResponse(json.dumps(basket_after), content_type="application/json")


def create_basket_test():
    info = BasketOnboardingInfo(people=1, budget=20, tags=["European", "Chinese", "Indian"], days="2",
                                supermarket=Supermarket.objects.get(name="tesco"))
    basket = BasketRecommendationEngine.create_onboarding_basket(info)

    # The structure of the recommendation engine response is a dictionnary
    # basket[selected_product] = [quantity_to_buy, abstract_product]
    ii = 0
    product_list = {}
    for product, quantity_abs in basket.iteritems():
        print ii, product, quantity_abs
        product_list["http://www.tesco.com" + str(product.link)] = str(int(quantity_abs[0]))
        ii += 1

    #basket_porting_test("some_request", product_list)


def check_basket_persistence(basket_before, basket_after):
    #if any item that should be in the basket_before isn't for some reason,
    #report it here
    for product_link, ported_or_not in basket_before.iteritems():
        try:
            dummy = basket_after[product_link]
        except KeyError:
            basket_after[product_link] = "False"

    return basket_after
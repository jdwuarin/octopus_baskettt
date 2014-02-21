from octopus_recommendation_engine.basket_recommendation_engine import \
    BasketRecommendationEngine
from octopus_user.models import UserSettings
from octopus_groceries.models import *
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.http import HttpResponse
import json


def basket_porting_test(request, product_list_before):

    SpiderManagerController.create_if_none()

    # for testing purposes
    email = "arnaudbenard13+test@gmail.com"
    password = "test123"

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               product_list_before, thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    #product_list is a list of type: [product, quantity]

    product_list_after = this_basket.thread_manager.get_response()
    product_list_after = check_basket_persistence(product_list_before,
                                                  product_list_after)

    #####################
    for key, value in product_list_after.iteritems():
        print key, value
    #####################

    response = []

    for product, is_success in product_list_after.iteritems():
        if not type(product[0]) == str:
            product_json = dict()
            product_json['id'] = product[0].id
            product_json['name'] = product[0].name
            product_json['price'] = product[0].price
            product_json['link'] = product[0].link
            product_json['img'] = str(product[0].external_image_link)
            product_json['quantity'] = product[1]
            product_json['success'] = is_success

        else:
            product_json['Response_status'] = is_success

        response.append(product_json)

    return HttpResponse(json.dumps(response), content_type="application/json")


def create_basket_test():

    user_settings = UserSettings(
                    people=2,
                    days=2,
                    price_sensitivity=0.23,
                    tags=["European", "Chinese", "Indian"],
                    default_supermarket=Supermarket.objects.get(name="tesco"),
                    pre_user_creation_hash="dummy",
                    diet=Diet.objects.all.get(name="vegan"),
                    banned_meats=[1, 3],
                    banned_abstract_products=[])

    basket = BasketRecommendationEngine.create_onboarding_basket(user_settings)

    # The structure of the recommendation engine response is a dictionnary
    # basket[selected_product] = [quantity_to_buy, abstract_product]
    ii = 0
    product_list = []
    for product, quantity_abs in basket.iteritems():
        print ii, product, quantity_abs
        product_list.append((product, str(int(quantity_abs[0]))))
        ii += 1

    basket_porting_test("some_request", product_list)

def check_basket_persistence(product_list_before, product_list_after):
    #if any item that should be in the product_list_before isn't for some reason,
    #report it here
    for product in product_list_before:
        try:
            dummy = product_list_after[product]
        except KeyError:
            product_list_after[product] = "False"

    return product_list_after
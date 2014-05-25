from octopus_recommendation_engine.basket_onboarding_info import BasketOnboardingInfo
from octopus_recommendation_engine.basket_recommendation_engine import BasketRecommendationEngine
from octopus_groceries.models import Tag, Product, TagRecipe, Supermarket
from octopus_basket.basket_to_port import BasketToPort
from octopus_basket.spider_manager import SpiderManagerController
from octopus_basket.thread_manager import ThreadManager
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
    product_list_after = check_basket_persistence(product_list_before, product_list_after)

    #####################
    for key, value in product_list_after.iteritems():
        print key, value
    #####################

    response = []

    for key, is_success in product_list_after.iteritems():
        product_json = dict()
        if not type(key) == str:
            product_json['id'] = key[0].id
            product_json['name'] = key[0].name
            product_json['price'] = key[0].price
            product_json['link'] = key[0].link
            product_json['img'] = str(key[0].external_image_link)
            product_json['quantity'] = key[1]
            product_json['success'] = is_success

        else:
            product_json[key] = is_success

        response.append(product_json)

    return HttpResponse(json.dumps(response), content_type="application/json")


def create_basket_test():

    products = Product.objects.all()[:10]

    # The structure of the recommendation engine response is a dictionnary
    # basket[selected_product] = [quantity_to_buy, abstract_product]
    product_list = []
    for ii, product, in enumerate(products):
        print ii, product
        product_list.append((product, str(1)))

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
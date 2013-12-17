from django.shortcuts import render
import json
from django.http import HttpResponse
from django.conf import settings
from basket_porting.basket_to_port import Basket_to_port
from basket_porting.spider_manager import Spider_manager_controller
from basket_porting.thread_manager import Thread_manager

from recommendation_engine.basket_onboarding_info import Basket_onboarding_info
from recommendation_engine.basket_recommendation_engine import Basket_recommendation_engine

def index(request):
    context = {'debug': settings.DEBUG}
    return render(request, 'products/index.html', context)

def spider_view(request):

    Spider_manager_controller.create_if_none()

    info = Basket_onboarding_info(people = 6, budget = 50, tags = ["Japanese", "European"], days = "")

    basket = Basket_recommendation_engine.create_onboarding_basket(info)

    product_details = {}

    # for entry in basket:

    #     print str(entry[0]) + ",ingredient:," + str(
    #          entry[1]) + ","  + str(int(entry[2])) 

    while len(basket) > 0:

        product , my_list= basket.popitem()
        print str(product) + ",ingredient:," + str(
            my_list[0]) + ","  + str(int(my_list[1]))

        
        # product_details[str("http://www.tesco.com" + product.link)] = str(int(quantity))

    # product_details = {
    #     "http://www.tesco.com/groceries/Product/Details/?id=4234": "1",
    #     "http://www.tesco.com/groceries/Product/Details/?id=268768585" : "1", 
    #     "http://www.tesco.com/groceries/Product/Details/?id=268595587" : "1", 
    #     "http://www.tesco.com/groceries/Product/Details/?id=255664065" : "1", 
    #     "http://www.tesco.com/groceries/Product/Details/?id=254881517" : "1", 
    #     "http://www.tesco.com/groceries/Product/Details/?id=261597383" : "1", 
    #     "http://www.tesco.com/groceries/Product/Details/?id=23424": "1",

    # }

    thread_manager = Thread_manager()
    this_basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123",
        product_details, thread_manager)

    # Spider_manager_controller.add_basket_to_port(this_basket)

    # this_basket.thread_manager.wait(15)

    response_data = this_basket.thread_manager.get_response() 
    return HttpResponse(json.dumps(response_data), content_type="application/json")




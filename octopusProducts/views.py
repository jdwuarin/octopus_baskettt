from django.shortcuts import render
import json
from django.http import HttpResponse
from django.conf import settings
from basket_porting.basket_to_port import Basket_to_port
from basket_porting.spider_manager import Spider_manager_controller
from basket_porting.thread_manager import Thread_manager
from django.utils import simplejson

from recommendation_engine.basket_onboarding_info import Basket_onboarding_info
from recommendation_engine.basket_recommendation_engine import Basket_recommendation_engine

def index(request):
    context = {'debug': settings.DEBUG}
    return render(request, 'products/index.html', context)

def spider_view(request):

    Spider_manager_controller.create_if_none()

    data = simplejson.loads(request.body)

    product_details = data['products'] # List of product generated by the user
    email = data['email']
    password = data['password']

    # for testing purposes
    email = "arnaudbenard13+test@gmail.com"
    password = "test123"


    thread_manager = Thread_manager()
    this_basket = Basket_to_port(request, email, password,
        product_details, thread_manager)

    Spider_manager_controller.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    response_data = this_basket.thread_manager.get_response() 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

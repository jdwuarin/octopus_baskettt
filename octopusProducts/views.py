from django.shortcuts import render
from scrapy import log

from twisted.internet import reactor
from basket_to_port import Basket_to_port
from reactor_thread_controller import Reactor_thread_controller


import json

from django.http import HttpResponse


def index(request):
    return render(request, 'products/index.html')



def spider_view(request):

    #start reactor_thread if not already started

    Reactor_thread_controller.create_and_start_thread()

    product_details = {"http://www.tesco.com/groceries/Product/Details/?id=268768585": "1"}

    basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123", product_details)

    Reactor_thread_controller.add_basket_to_port(basket)


    response_data = {} 
    response_data['itemAddedToBasket'] = 'False'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def start_reactor(request):
    if not reactor.running:
        reactor.run(installSignalHandlers=False)


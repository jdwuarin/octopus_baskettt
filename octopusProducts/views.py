from django.shortcuts import render
from scrapy import log

from twisted.internet import reactor
from basket_to_port import Basket_to_port
from scrapy import log
import json
from django.http import HttpResponse

from spider_manager import Spider_manager_controller

def index(request):
    return render(request, 'products/index.html')

def spider_view(request):

    Spider_manager_controller.create_if_none()

    product_details = {"http://www.tesco.com/groceries/Product/Details/?id=2687685852": "1",}

    basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123", product_details)

    Spider_manager_controller.add_basket_to_port(basket)

    response_data = {} 
    response_data['itemAddedToBasket'] = 'False'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

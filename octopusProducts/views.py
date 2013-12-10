from django.shortcuts import render
from scrapy import log

from basket_to_port import Basket_to_port
from scrapy import log
import json
from django.http import HttpResponse

from spider_manager import Spider_manager_controller

from threading import Condition

def index(request):
    return render(request, 'products/index.html')

def spider_view(request):

    Spider_manager_controller.create_if_none()

    product_details = {
        "http://www.tesco.com/groceries/Product/Details/?id=4234": "1",
        "http://www.tesco.com/groceries/Product/Details/?id=23424": "1",

    }

    basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123", product_details)

    Spider_manager_controller.add_basket_to_port(basket)

    #this threading solution with appropriate wake up
    #will work. To code tomorrow.
    # DummyClass()

    response_data = {} 
    response_data['itemAddedToBasket'] = 'False'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class DummyClass(object):
    i = 0
    lock = Condition()

    def __new__(cls):
        cls.i = cls.i + 1
        if cls.i % 2 == 1:
            while True:
                cls.lock.acquire()
                cls.lock.wait(15.0)

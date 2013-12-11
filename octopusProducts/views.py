from django.shortcuts import render
import json
from django.http import HttpResponse
from django.conf import settings
from basket_porting.basket_to_port import Basket_to_port
from basket_porting.spider_manager import Spider_manager_controller
from basket_porting.thread_manager import Thread_manager

def index(request):
    context = {'debug': settings.DEBUG}
    return render(request, 'products/index.html', context)

def spider_view(request):

    Spider_manager_controller.create_if_none()

    product_details = {
        "http://www.tesco.com/groceries/Product/Details/?id=4234": "1",
        "http://www.tesco.com/groceries/Product/Details/?id=268768585" : "1", 
        "http://www.tesco.com/groceries/Product/Details/?id=268595587" : "1", 
        "http://www.tesco.com/groceries/Product/Details/?id=255664065" : "1", 
        "http://www.tesco.com/groceries/Product/Details/?id=254881517" : "1", 
        "http://www.tesco.com/groceries/Product/Details/?id=261597383" : "1", 
        "http://www.tesco.com/groceries/Product/Details/?id=23424": "1",

    }

    thread_manager = Thread_manager()
    this_basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123",
        product_details, thread_manager)

    Spider_manager_controller.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    response_data = this_basket.thread_manager.get_response() 
    return HttpResponse(json.dumps(response_data), content_type="application/json")



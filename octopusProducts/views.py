from django.shortcuts import render
from scrapy import log

from basket_to_port import Basket_to_port
from scrapy import log
import json
from django.http import HttpResponse

from spider_manager import Spider_manager_controller

from threading import Event

def index(request):
    return render(request, 'products/index.html')

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

    current_thread_manager = Current_thread_manager()
    this_basket = Basket_to_port(request, "arnaudbenard13+test@gmail.com", "test123",
        product_details, current_thread_manager)

    Spider_manager_controller.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    response_data = this_basket.thread_manager.get_response() 
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class Current_thread_manager(object):

    def __init__(self):
        self.lock = Event()
        self.response = None

    def wait(self, server_timeout_time):
        self.lock.wait(server_timeout_time)

    def build_response(self, successful_item_list, failed_item_list):
        self.response = {}
        self.response['Response_status'] = 'no_timeout'
        for item in successful_item_list:
            self.response[item] = "True"
        for item in failed_item_list:
            self.response[item] = "False"

    def get_response(self):
        if self.response is None:
            self.response = {}
            self.response['Response_status'] = 'server_timeout'

        return self.response


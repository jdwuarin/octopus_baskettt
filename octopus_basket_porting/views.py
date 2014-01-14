import json
from django.http import HttpResponse
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import Spider_manager_controller
from octopus_basket_porting.thread_manager import ThreadManager


def port_basket(request):

    Spider_manager_controller.create_if_none()

    data = json.loads(request.body)

    product_details = data['products']  # List of product generated by the user
    email = data['email']
    password = data['password']

    product_list = {}

    for product in product_details:
        product_list["http://www.tesco.com" + str(product['link'])] = str(int(product['quantity']))

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               product_list, thread_manager)

    Spider_manager_controller.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    response_data = this_basket.thread_manager.get_response()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
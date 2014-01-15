import json
from django.http import HttpResponse
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.contrib.auth.decorators import login_required

@login_required
def port_basket(request):

    SpiderManagerController.create_if_none()

    data = json.loads(request.body)

    product_details = data['products']  # List of product generated by the user
    email = data['email']
    password = data['password']

    basket_before_porting = {}

    for product in product_details:
        basket_before_porting["http://www.tesco.com" + str(product['link'])] = str(int(product['quantity']))

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               basket_before_porting, thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    basket_after_porting = this_basket.thread_manager.get_response()
    basket_after_porting = check_basket_persistence(basket_before_porting, basket_after_porting)

    return HttpResponse(json.dumps(basket_after_porting), content_type="application/json")


def check_basket_persistence(basket_before, basket_after):
    #if any item that should be in the basket_before_porting isn't for some reason,
    #report it here
    for product_link, ported_or_not in basket_before.iteritems():
        try:
            dummy = basket_after[product_link]
        except KeyError:
            basket_after[product_link] = "False"

    return basket_after
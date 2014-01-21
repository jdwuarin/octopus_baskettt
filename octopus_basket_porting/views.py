import json
from django.http import HttpResponse
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.contrib.auth.decorators import login_required
from octopus_groceries.models import Product
from octopus_user.models import UserRecommendedBasket, UserGeneratedBasket


@login_required
def port_basket(request):
    SpiderManagerController.create_if_none()
    data = json.loads(request.body)

    #first determine what user made this request
    user = request.user

    #first save the user settings if user is new
    # settings = data['settings']
    # if not settings == "False":
    #     #some settings have changed
    #     user_settings = UserSettings(user=user,
    #                                  num_people=data['people'],
    #                                  num_days=data['days'],
    #                                  budget=data['budget'])
    #     user_settings.save()

    #then save the basket recommended to the user
    recommended_basket = data['recommendation']
    rb_product_dict = {}
    for product in recommended_basket:
        rb_product_dict[str(product['id'])] = str(product['quantity'])

    user_recommended_basket = UserRecommendedBasket(user=user,
                                                    product_dict=
                                                    rb_product_dict)
    user_recommended_basket.save()

    #then save the basket generated by the user based on recommendation
    user_generated_basket = data['products']
    ugb_product_dict = {}
    for product in user_generated_basket:
        ugb_product_dict[str(product['id'])] = str(product['quantity'])

    user_recommended_basket = UserGeneratedBasket(user=user,
                                                  product_dict=ugb_product_dict,
                                                  user_recommended_basket=
                                                  user_recommended_basket)
    user_recommended_basket.save()

    email = data['email']
    password = data['password']
    user_generated_basket_before_porting = []

    for product in user_generated_basket:
        user_generated_basket_before_porting.append(
            (Product.objects.get(id=product['id']),
             str(int(product['quantity']))))

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               user_generated_basket_before_porting,
                               thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(15)

    user_generated_basket_after_porting = this_basket.thread_manager.get_response()
    user_generated_basket_after_porting = check_basket_persistence(
        user_generated_basket_before_porting,
        user_generated_basket_after_porting)

    response = []
    for product, is_success in user_generated_basket_after_porting.iteritems():
        if not type(product[0]) == str:
            product_json = dict()
            product_json['id'] = product[0].id
            product_json['name'] = product[0].name
            product_json['price'] = product[0].price
            product_json['link'] = product[0].link
            product_json['img'] = str(product[0].external_image_link)
            product_json['quantity'] = product[1]
            product_json['success'] = is_success

        else:
            product_json['Response_status'] = is_success

        response.append(product_json)

    return HttpResponse(json.dumps(response), content_type="application/json")


def check_basket_persistence(product_list_before, product_list_after):
    #if any item that should be in the product_list_before isn't for some reason,
    #report it here
    for product in product_list_before:
        try:
            dummy = product_list_after[product]
        except KeyError:
            product_list_after[product] = "False"

    return product_list_after
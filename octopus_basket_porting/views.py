import json
from django.http import HttpResponse
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.contrib.auth.decorators import login_required
from octopus_groceries.models import Product, Tag
from octopus_user.models import UserRecommendedBasket, UserGeneratedBasket, \
    UserSettings


@login_required
def port_basket(request):
    SpiderManagerController.create_if_none()
    data = json.loads(request.body)

    #first determine what user made this request
    user = request.user

    # first save the user settings if user is new
    settings = data['settings']
    tags = []
    for tag in settings['cuisine']:
        if tag == "Italian" or tag == "French" or (
            tag == "Spanish"):
            tags.append(Tag.objects.get(name="European").id)
        else:
            tags.append(Tag.objects.get(name=tag).id)

    if not settings == "False":
        #some settings have changed
        try:
            user_settings = UserSettings.objects.get(user=user)
            user_settings.people = settings['people']
            user_settings.days = settings['days']
            user_settings.budget = settings['budget']
            user_settings.tags = tags
            user_settings.save()
        except UserSettings.DoesNotExist:
            user_settings = UserSettings(user=user,
                                         people=settings['people'],
                                         days=settings['days'],
                                         budget=settings['budget'],
                                         tags=tags)
            user_settings.save()

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
    user_generated_basket_list = data['products']
    ugb_product_dict = {}
    for product in user_generated_basket_list:
        ugb_product_dict[str(product['id'])] = str(product['quantity'])

    user_generated_basket = UserGeneratedBasket(user=user,
                                                product_dict=ugb_product_dict,
                                                user_recommended_basket=
                                                user_recommended_basket)
    user_generated_basket.save()

    email = data['email']
    password = data['password']
    user_generated_basket_before_porting = []

    for product in user_generated_basket_list:
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

    # key[0] is the Product item or a string and. If product item, key[1]
    # is the quantity to order
    for key, is_success in user_generated_basket_after_porting.iteritems():
        product_json = dict()
        if not type(key) == str:
            product_json['id'] = key[0].id
            product_json['name'] = key[0].name
            product_json['price'] = key[0].price
            product_json['link'] = key[0].link
            product_json['img'] = str(key[0].external_image_link)
            product_json['quantity'] = key[1]
            product_json['success'] = is_success

        else:
            product_json[key] = is_success

        response.append(product_json)

    # frontend needs to check for "Response_status" == "server_timeout" and
    # "good_login" == "False" in that order before anything else
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

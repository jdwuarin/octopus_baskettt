import json
from django.http import HttpResponse
from octopus_basket_porting.basket_to_port import BasketToPort
from octopus_basket_porting.spider_manager import SpiderManagerController
from octopus_basket_porting.thread_manager import ThreadManager
from django.contrib.auth.decorators import login_required
from octopus_groceries.models import Product, Tag
from octopus_user.models import UserRecommendedBasket, UserGeneratedBasket, \
    UserSettings
from octopus_basket_porting.pipelines import BadLoginException
import octopus_recommendation_engine.helpers


@login_required
def port_basket(request):
    SpiderManagerController.create_if_none()
    data = json.loads(request.body)
    user_settings_hash = data['user_settings_hash']

    # first determine what user made this request
    user = request.user


    # then save the user settings if user is new
    try:
        # try seeing if user already has settings assigned to self
        user_settings = UserSettings.objects.get(user=user)
        # it exists, so try to delete the one created anonymously during
        # the first basket creation that was stupidly created by the user
        # who already had an account
        try:
            user_settings = UserSettings.objects.get(
                pre_user_creation_hash=user_settings_hash)
            user_settings.delete()

        except UserSettings.DoesNotExist:
            # no problem, there actually was no hash or it was already deleted
            pass

    except UserSettings.DoesNotExist:
        #could not find user settings, report that
        return HttpResponse("Cannot find user settings",
                                content_type="application/json")


    recommended_basket = data['recommended_basket']
    user_recommended_basket = None
    # save the basket recommended to user if the id did not exist
    if not data['recommended_basket_id']:
        user_recommended_basket = octopus_recommendation_engine.\
            helpers.create_user_recommended_basket_from_basket(
            recommended_basket, user)

        user_recommended_basket.save()

    #else just get it by id
    else:
        urb_id = data['recommended_basket_id']
        user_recommended_basket = UserRecommendedBasket(id=urb_id)

    #then save the basket generated by the user based on recommendation
    generated_basket = data['products']
    user_generated_basket = octopus_recommendation_engine.\
        helpers.create_user_generated_basket_from_basket(
        generated_basket, user_recommended_basket, user)


    email = data['email']
    password = data['password']
    user_generated_basket_before_porting = []

    for product in generated_basket:
        user_generated_basket_before_porting.append(
            (Product.objects.get(id=product['id']),
             str(int(product['quantity']))))

    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               user_generated_basket_before_porting,
                               thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(20)

    user_generated_basket_after_porting = this_basket.thread_manager.get_response()

    # make sure user could login to tesco. if not, notify user.
    if user_generated_basket_after_porting['server_timeout'] =='True' or \
                    user_generated_basket_after_porting['good_login'] == "False":
       return HttpResponse(json.dumps(
           user_generated_basket_after_porting), content_type="application/json")

    user_generated_basket_after_porting = check_basket_persistence(
        user_generated_basket_before_porting,
        user_generated_basket_after_porting)

    response = {}
    response_product_list = []

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
            response_product_list.append(product_json)

        else:
            # the server status and good_login status
            response[key] = is_success

    # the product list
    response['product_list'] = response_product_list

    #only save user_generated basket once we know it has been ported
    user_generated_basket.save()
    octopus_recommendation_engine.\
        helpers.apply_email_sending_date(UserSettings.objects.get(user=user))

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

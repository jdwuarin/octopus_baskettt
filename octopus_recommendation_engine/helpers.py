import string
import random
from haystack.query import SearchQuerySet
from octopus_groceries.models import *
from octopus_user.models import *
from datetime import date, timedelta, datetime


def get_user_settings_from_user(user, data):

        # get user_settings
    user_settings = None
    if user.is_authenticated():
        try:
            user_settings = UserSettings.objects.get(user=user)
        except:
            pass

    #None may be returned as user_settings
    return user_settings


def get_json_basket(basket):

    response = []

    # basket[0] = [[selected_product, quantity], other_prod1, op2,...]

    for entry in basket:
        # this is the json that will be returned
        product_json = {}

        # this is the main product, the one to be shown by default
        product_json_main = {}
        product_json_main['id'] = entry[0][0].id
        product_json_main['name'] = entry[0][0].name
        product_json_main['price'] = entry[0][0].price
        product_json_main['link'] = entry[0][0].link
        product_json_main['img'] = str(entry[0][0].external_image_link)
        # product_json_main['ingredient'] = entry[0][0].ingredients

        department = entry[0][0].department
        product_json_main['department'] = (
            "other" if department is None else department.name)
        # aisle = entry[0][0].aisle
        # product_json_main['aisle'] = (
            # "other" if aisle is None else aisle.name)
        # category = entry[0][0].category
        # product_json_main['category'] = (
            # "other" if category is None else category.name)

        product_json['main'] = product_json_main
        product_json['quantity'] = int(entry[0][1])
        other_products = []

        for ii in range(1, len(entry)):
            product_json_other = {}
            product_json_other['id'] = entry[ii].id
            product_json_other['name'] = entry[ii].name
            product_json_other['price'] = entry[ii].price
            product_json_other['link'] = entry[ii].link
            product_json_other['img'] = str(entry[ii].external_image_link)

            # product_json_other['ingredient'] = entry[ii].ingredients
            # department = entry[ii].department
            product_json_other['department'] = (
                "other" if department is None else department.name)
            # aisle = entry[ii].aisle
            # product_json_other['aisle'] = (
                # "other" if aisle is None else aisle.name)
            # category = entry[ii].category
            # product_json_other['category'] = (
                # "other" if category is None else category.name)

            other_products.append(product_json_other)

        product_json['other_products'] = other_products
        response.append(product_json)

    return response


def create_user_recommended_basket_from_basket(basket, user):
    rb_product_dict = {}
    for entry in basket:
        # if it is not the hash added at end of list in the list sent
        if len(entry) > 1:
            rb_product_dict[str(entry['main']['id'])] = str(entry['quantity'])

    # user_recommended_basket = UserRecommendedBasket(user=user,
    #                                                 product_dict=
    #                                                 rb_product_dict)
    # return user_recommended_basket


def create_user_generated_basket_from_basket(basket,
                                             user_recommended_basket, user):
    ugb_product_dict = {}
    for product in basket:
        ugb_product_dict[str(product['id'])] = str(product['quantity'])

    # user_generated_basket = UserGeneratedBasket(user=user,
    #                                             product_dict=ugb_product_dict,
    #                                             user_recommended_basket=
    #                                             user_recommended_basket)

    # return user_generated_basket


def get_basket_from_user_recommended_basket(urb):
    basket = []
    #recommended_basket product_dict
    rb_product_dict = {}
    for urb_id, quantity in urb.product_dict.iteritems():
        try:
            product = Product.objects.get(id=urb_id)
            basket.append([[product, quantity]])
        except Product.DoesNotExist:
            pass

    return basket


def apply_email_sending_date(user_settings):

    user_settings.next_recommendation_email_date = \
        date.today() + timedelta(days=user_settings.days)

    user_settings.save()
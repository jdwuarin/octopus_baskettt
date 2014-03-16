import json
import string
import random
from haystack.query import SearchQuerySet
from octopus_groceries.models import *
from octopus_user.models import *
from django.http import HttpResponse
from django.conf import settings


# Function that finds the client http host and returns the right url
def get_client_url(request):
    if not request:
        return ""
    else:
        http_string = 'http://' if settings.DEBUG  else 'https://'
        return http_string + request.META["HTTP_HOST"] + '/'


def get_list_from_comma_separated_string(comma_separated_string):

    # first get rid of the [ and ] form string
    comma_separated_string = comma_separated_string[1:-1]
    # the create the list from the string

    return_list = comma_separated_string.split(", ")

    return return_list


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
        product_json['quantity'] = entry[0][1]
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


def save_anonymous_basket_user_settings(data):
    key_error = False
    value_error = False

    user_hash = ''.join(random.choice(
        string.ascii_letters + string.digits) for x in range(60))

    user_settings = None
    try:
        cuisine_ids = []
        for cuisine in data['cuisine']:
                # make sure requested tag actually exists
            sqs = SearchQuerySet().filter(
                content=cuisine).models(Tag)
            if sqs:
                # just take the first one if there is some collision because of
                # some ransom buggy reason. This shouldn't be the case
                cuisine_ids.append(Tag.objects.filter(name=cuisine)[0].id)
            else:
                value_error = True
                break

        # TODO fix this bullshit
        banned_meats = []
        # for banned_meat in data['banned_meats']:
        #     id = BannableMeats.objects.get(name=banned_meat).id
        #     banned_meats.append(id)


        data['diet'] = "Normal"

        banned_abstract_products = []
        # for entry in data['banned_abstract_products']:
        #     sqs = SearchQuerySet().models(AbstractProduct)
        #     id = sqs.filter(content=entry)[0].object.id
        #     banned_abstract_products.append(id)

        ############################

        data['supermarket'] = "tesco" #TODO remove tesco hardcode

        if not value_error:
            user_settings = UserSettings(
                people=int(data['people']),
                days=int(data['days']),
                price_sensitivity=float(data['price_sensitivity']),
                tags=cuisine_ids,
                default_supermarket=
                Supermarket.objects.get(name=data['supermarket']),
                pre_user_creation_hash=user_hash,
                diet=Diet.objects.get(name=data['diet']),
                banned_meats=banned_meats,
                banned_abstract_products=banned_abstract_products)
            user_settings.save()
            # this is done to make sure the object is as it would be
            # from getting it form anywhere in the code considering the lists
            # are extracted as strings
            user_settings = UserSettings.objects.get(
                pre_user_creation_hash=user_hash)

    except KeyError:
        key_error = True
    except ValueError:
        value_error = True
    except IndexError:
        value_error = True

    no_success_condition = value_error or (
        key_error) or (
        int(data['people']) < 1) or (
        int(data['days']) < 1) or (
        float(data['price_sensitivity']) < 0) or (
        float(data['price_sensitivity']) > 1) or (
        len(data['cuisine']) < 1)

    if no_success_condition:
        return None
    else:
        return user_settings

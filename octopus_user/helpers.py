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

    # first get rid of the [ and ] from string
    comma_separated_string = comma_separated_string[1:-1]
    # then create the list from the string

    return_list = comma_separated_string.split(", ")

    return return_list


def save_user_settings(user, user_settings_hash):

    user_settings = None
    try:
        user_settings = UserSettings.objects.get(
            pre_user_creation_hash=user_settings_hash)
        user_settings.user = user
        user_settings.pre_user_creation_hash = None
        user_settings.save()

    # if there is no user_settings for this hash, this is a problem
    # deal with it in except block
    except UserSettings.DoesNotExist:
        pass

    return user_settings #will be none if user_settings is not found
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
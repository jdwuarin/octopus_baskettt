import json
import string
import random
from haystack.query import SearchQuerySet

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from octopus_groceries.models import *
from tastypie.authentication import SessionAuthentication
from octopus_recommendation_engine.basket_recommendation_engine import \
    BasketRecommendationEngine
from django.http import HttpResponse
from user_objects_only_authorization import UserObjectsOnlyAuthorization
from octopus_user.models import UserGeneratedBasket, UserInvited, UserSettings


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'email',
                  'date_joined']  # we can either whitelist like this or blacklist using exclude
        allowed_methods = ['get']
        resource_name = 'user'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authorization = UserObjectsOnlyAuthorization()
        authentication = SessionAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),

            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),

            url(r'^(?P<resource_name>%s)/signup%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name='api_signup'),

            url(r'^(?P<resource_name>%s)/current%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('current'), name='api_current'),

            url(r'^(?P<resource_name>%s)/basket%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('basket'), name='api_basket'),

            url(r'^(?P<resource_name>%s)/beta_subscription%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('beta_subscription'),
                name='api_beta_subscription'),
        ]

    def login(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(username=email, password=password)

        #check if user already ported a basket in the past
        user_generated_basket = UserGeneratedBasket.objects.filter(
            user=user)[:1]

        if user_generated_basket:
            has_history = True
        else:
            has_history = False

        if user:
            if user.is_active:
                login(request, user)

                return self.create_response(request, {
                    #redirect to a success page
                    'success': True,
                    'has_history': has_history
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False},
                                        HttpUnauthorized)

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        try:
            user_invited = UserInvited.objects.get(email__iexact=email)
            if not user_invited.is_invited:
                # user has already tried signing up but we have
                # not allowed him to use our beta yet. I.e, user is
                # not invited
                return HttpResponse('Unauthorized', status=401)
        except UserInvited.DoesNotExist:
            # user is not yet in the userInvited list
            # we add him with the is_invited flag set to False
            # we return a success false as user could not sign up
            user_invited = UserInvited(email=email, is_invited=False)
            user_invited.save()
            return self.create_response(request, {
                'reason': 'added, but not_invited',
                'success': False
            })

        # make sure user doesn't already exist using
        # case insensitive email as username
        try:
            User.objects.get(username__iexact=email)

            return self.create_response(request, {
                #user with same email address already exists
                'reason': 'already_exist',
                'success': False
            })

        except User.DoesNotExist:
            try:
                # then create user
                User.objects.create_user(email, email, password)

            except IntegrityError:
                # some error occured, return success False
                return self.create_response(request, {
                    #some other error occured
                    'reason': 'unindentified error',
                    'success': False
                })


        # Login after registration
        user = authenticate(username=email, password=password)
        login(request, user)

        # user successfully signup
        return self.create_response(request, {
            'success': True
        })

    # Get the current user
    def current(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        if request.user.is_authenticated():
            return self.create_response(request, {
                'success': True
            })
        else:
            # Anonymous users.
            return self.create_response(request, {
                'success': False
            })

    # Recommendation engine
    def basket(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        if request.user.is_authenticated():
            return self.registered_basket(request, **kwargs)
        else:
            return self.anonymous_basket(request, **kwargs)

    #get basket for someone who has noa ccount yet.
    def anonymous_basket(self, request, **kwargs):
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        key_error = False
        value_error = False

        hash = ''.join(random.choice(
            string.ascii_letters + string.digits) for x in range(60))

        user_settings = None
        try:
            #this is a hot fix for the fact that
            #the only tag for european type cuisines that exists is "European"
            real_cuisines = []
            for cuisine in data['cuisine']:
                if cuisine == "Italian" or cuisine == "French" or (
                    cuisine == "Spanish"):
                    real_cuisines.append("European")
                else:
                    # make sure requested tag actually exists
                    sqs = SearchQuerySet().filter(
                        content=cuisine).models(Tag)
                    if sqs:
                        real_cuisines.append(cuisine)
                    else:
                        value_error = True
                        break

            # TODO fix this bullshit
            banned_meats = []
            # for banned_meat in data['banned_meats']:
            #     id = BannableMeats.objects.get(name=banned_meat).id
            #     banned_meats.append(id)

            
            data['diet'] = "Vegan"

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
                    tags=real_cuisines,
                    default_supermarket=
                    Supermarket.objects.get(name=data['supermarket']),
                    pre_user_creation_hash=hash,
                    diet=Diet.objects.get(name=data['diet']),
                    banned_meats=banned_meats,
                    banned_abstract_products=banned_abstract_products)
                user_settings.save()

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
            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                                content_type="application/json")

        basket = BasketRecommendationEngine.create_onboarding_basket(
            user_settings)

        response = []

        # basket[0] = [[selected_product, quantity], other_prod1, op2,...]

        print "basket length: " + str(len(basket))

        for entry in basket:

            # this is the json that will be returned
            product_json = {}

            # this is the main product, the one to be showed by default
            product_json_main = {}
            product_json_main['id'] = entry[0][0].id
            product_json_main['name'] = entry[0][0].name
            product_json_main['price'] = entry[0][0].price
            product_json_main['link'] = entry[0][0].link
            product_json_main['img'] = str(entry[0][0].external_image_link)
            product_json_main['ingredient'] = entry[0][0].ingredients

            product_json['main'] = (product_json_main)
            product_json['quantity'] = entry[0][1]
            other_products = []

            for ii in range(1, len(entry)):
                product_json_other = {}
                product_json_other['id'] = entry[ii].id
                product_json_other['name'] = entry[ii].name
                product_json_other['price'] = entry[ii].price
                product_json_other['link'] = entry[ii].link
                product_json_other['img'] = str(entry[ii].external_image_link)
                product_json_other['ingredient'] = entry[ii].ingredients

                other_products.append(product_json_other)

            product_json['other_products'] = other_products
            response.append(product_json)

        user_settings_hash_json = {}
        user_settings_hash_json['user_settings_hash'] = hash
        response.append(user_settings_hash_json)
        data = json.dumps(response)

        return HttpResponse(data, content_type="application/json")


    # get basket for someone who already has an account
    def registered_basket(self, request, **kwargs):
        pass

    def beta_subscription(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        email = data['email']

        response_data = {}

        try:
            user_invited = UserInvited.objects.get(email__iexact=email)
            response_data['success'] = False
            response_data['reason'] = "user already exists"
        except UserInvited.DoesNotExist:
            user_invited = UserInvited(email=email, is_invited=False)
            user_invited.save()
            response_data['success'] = True

        response_data = json.dumps(response_data)
        return HttpResponse(response_data, content_type="application/json")

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
            user_invited = UserInvited.objects.get(email=email)
            if not user_invited.is_invited:
                return HttpResponse('Unauthorized', status=401)
        except UserInvited.DoesNotExist:
            return HttpResponse('Unauthorized', status=401)

        try:
            User.objects.create_user(email, email, password)

        except IntegrityError:
            print "User already exits"
            return self.create_response(request, {
                #user with same email address already exists
                'success': False
            })

        # Login after registration
        user = authenticate(username=email, password=password)
        login(request, user)

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

            banned_meats = []
            for banned_meat in data['banned_meats']:
                id = BannableMeats.objects.get(name=banned_meat).id
                banned_meats.append(id)

            banned_abstract_products = []
            for entry in data['banned_abstract_products']:
                sqs = SearchQuerySet().models(AbstractProduct)
                id = sqs.filter(content=entry)[0].object.id
                banned_abstract_products.append(id)

            data['supermarket'] = Supermarket.objects.get(
            name="tesco") #TODO remove tesco hardcode

            if not value_error:
                user_settings = UserSettings(
                    people=int(data['people']),
                    days=int(data['days']),
                    price_sensitivity=float(data['price_sensitivity']),
                    tags=real_cuisines,
                    default_supermarket=
                    data['supermarket'],
                    pre_user_creation_hash=hash,
                    diet=Diet.objects.all.get(name=data['diet']),
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

        # The structure of the recommendation engine response is a dictionnary
        # basket[selected_product] = [quantity_to_buy, abstract_product]
        for key, value in basket.iteritems():
            product_json = {}
            product_json['id'] = key.id
            product_json['name'] = key.name
            product_json['price'] = key.price
            product_json['link'] = key.link
            product_json['img'] = str(key.external_image_link)
            product_json['quantity'] = value[0]
            product_json['ingredient'] = value[1].name
            response.append(product_json)

        user_settings_hash_json = {}
        user_settings_hash_json['user_settings_hash'] = hash
        response.append(user_settings_hash_json)
        data = json.dumps(response)

        return HttpResponse(data, content_type="application/json")

    # get basket for someone who already has an account
    def registered_basket(self, request, **kwargs):
        pass
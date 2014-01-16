from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from octopus_groceries.models import Supermarket
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from octopus_recommendation_engine.basket_onboarding_info import BasketOnboardingInfo
from octopus_recommendation_engine.basket_recommendation_engine import BasketRecommendationEngine
from django.http import HttpResponse
from user_objects_only_authorization import UserObjectsOnlyAuthorization
import json


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'email', 'date_joined']  # we can either whitelist like this or blacklist using exclude
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
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print "logged in"
                return self.create_response(request, {
                    #redirect to a success page
                    'success': True
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
            print request.user
            print request.session
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

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

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        key_error = False
        value_error = False

        try:
            dummy = int(data['budget'])
            dummy = int(data['people'])
            dummy = data['cuisine']
            dummy = int(data['days'])
        except KeyError:
            key_error = True
        except ValueError:
            value_error = True

        no_success_condition = value_error or \
                               key_error or \
                               int(data['budget']) < 1 or \
                               len(data['cuisine']) < 1 or \
                               int(data['days']) < 1 or \
                               int(data['people']) < 1

        if no_success_condition:
            no_success = json.dumps({'success': False})
            print "no_success"
            return HttpResponse(no_success,
                                content_type="application/json")

        #this is a hot fix for the fact that
        #the only tag for european type cuisines that exists is "European"
        real_cuisines = []
        for cuisine in data['cuisine']:
            if cuisine == "Italian" or cuisine == "French" or cuisine == "Spanish":
                real_cuisines.append("European")
            else:
                real_cuisines.append(cuisine)
        data['cuisine'] = real_cuisines

        data['supermarket'] = Supermarket.objects.get(name="tesco") #remove tesco hardcode

        onboarding_info = BasketOnboardingInfo(people=data['people'], budget=data['budget'],
                                               tags=data['cuisine'], days=data['days'],
                                               supermarket=data['supermarket'])

        basket = BasketRecommendationEngine.create_onboarding_basket(onboarding_info)

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

        data = json.dumps(response)

        return HttpResponse(data, content_type="application/json")
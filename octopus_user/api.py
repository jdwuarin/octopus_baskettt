from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from octopus_groceries.models import Product, Recipe
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from octopus_recommendation_engine.basket_onboarding_info import BasketOnboardingInfo
from octopus_recommendation_engine.basket_recommendation_engine import BasketRecommendationEngine
from django.http import HttpResponse
import json


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['email', 'date_joined'] #we can either whitelist like this or blacklist using exclude
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authorization = DjangoAuthorization() #these are relevant to the API and who can access these parts of the API
        authentication = SessionAuthentication() #in other views, it would be required of us to add the "@login_required" decoration

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
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )


    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        if request.user and request.user.is_authenticated():
            print request.user
            print request.session
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        try:
            User.objects.create_user(email, '', password)

        except IntegrityError:
            print "User already exits"
            return self.create_response(request, {
                #user with same email adress already exists
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

        try:
            data['budget']
            data['people']
            data['cuisine']
            pass
        except KeyError:
            key_error = True

        if  key_error or int(data['budget'])< 1 or len(data['cuisine']) < 1 or(
            int(data['days'])<1):

            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                content_type="application/json")

        onboarding_info = BasketOnboardingInfo(people = data['people'], budget = data['budget'],
            tags = data['cuisine'], days = data['days'])

        basket = BasketRecommendationEngine.create_onboarding_basket(onboarding_info)

        response = []

        # The structure of the recommendation engine response is a dictionnary
        # product_list[selected_product] = [quantity_to_buy, ingredient]
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


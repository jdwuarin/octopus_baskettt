import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from octopus_recommendation_engine.basket_recommendation_engine import \
    BasketRecommendationEngine
from django.http import HttpResponse
from user_objects_only_authorization import UserObjectsOnlyAuthorization
from octopus_user.models import *
import helpers


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
            return self.get_later_basket(request, **kwargs)
        else:
            return self.get_first_basket(request, **kwargs)

    #get basket for someone who has no ccount yet.
    def get_first_basket(self, request, **kwargs):
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))
        # get user_settings
        user_settings = None
        if request.user.is_authenticated():
            try:
                user_settings = UserSettings.objects.get(user=request.user)
            except:
                pass
        else:
            user_settings = helpers.save_anonymous_basket_user_settings(data)

        if not user_settings:
            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                                content_type="application/json")

        print user_settings
        # get basket from user_settings
        basket = BasketRecommendationEngine.create_onboarding_basket(
            user_settings)

        # create response from basket
        response = helpers.get_json_basket(basket)

        # add hash to response
        user_settings_hash_json = {}
        user_settings_hash_json[
            'user_settings_hash'] = user_settings.pre_user_creation_hash
        response.append(user_settings_hash_json)

        data = json.dumps(response)
        return HttpResponse(data, content_type="application/json")


    # get basket for someone who already has an account
    def get_later_basket(self, request, **kwargs):
        user = request.user

        # see if user has some baskets
        ugb = UserGeneratedBasket.objects.filter(user=user).order_by('-time')
        urb = UserRecommendedBasket.objects.filter(user=user).order_by('-time')

        if ugb:
            # if so, take last and just remove 20% switching them with similar
            # in similar ailse (yes, this is sort of a shitty hack)
            last_ugb = ugb[len(ugb)-1]
            basket = []
            for id, quantity in last_ugb.product_dict.iteritems():
                try:
                    product = Product.objects.get(id=id)
                    basket.append([[product, quantity]])
                except Product.DoesNotExist:
                    pass
            if basket:
                response = helpers.get_json_basket(basket)
                data = json.dumps(response)
                return HttpResponse(data, content_type="application/json")
            else:
                no_success = json.dumps({'success': False})
                return HttpResponse(no_success,
                                    content_type="application/json")

        else:
            # no basket yet, just create an anonymous one.
            return self.get_first_basket(request, **kwargs)


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

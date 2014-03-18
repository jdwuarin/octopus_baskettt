import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from octopus_recommendation_engine import basket_recommendation_engine
from django.http import HttpResponse
from user_objects_only_authorization import UserObjectsOnlyAuthorization
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_done
from django import forms
from octopus_user.models import *
import helpers

from django.contrib.auth.forms import  PasswordResetForm

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

            url(r'^(?P<resource_name>%s)/password/reset%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('password_reset_cb'),
                name='api_password_reset'),

            url(r'^(?P<resource_name>%s)/password/reset/done%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('password_reset_done_cb'), name='api_password_reset_done'),

            url(r'^(?P<resource_name>%s)/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})%s$' %
                (self._meta.resource_name, trailing_slash()),
               self.wrap_view('password_reset_confirm_cb'),
                name='api_password_reset_confirm'),


            url(r'^(?P<resource_name>%s)/password/done%s$' %
                (self._meta.resource_name, trailing_slash()),
                'django.contrib.auth.views.password_reset_complete', name='api_password_reset_complete'),
        ]

    def password_reset_confirm_cb(self, request, **kwargs):
        print "tttta mare"
        print request
        return password_reset_confirm(request,
            post_reset_redirect='api/v1/user/password/reset/done/',
            uidb64=kwargs["uidb64"],
            token=kwargs["token"])

    def password_reset_cb(self, request, **kwargs):
        return password_reset(request,
            post_reset_redirect='/done/',
            email_template_name='password_reset_email.html')

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

        # get basket from user_settings and data
        basket, user_settings = (
            basket_recommendation_engine.create_onboarding_basket(
                request.user, data))

        # if failure, say so
        if not basket or not user_settings :
            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                                content_type="application/json")

        # create response from basket
        response = {}
        response['recommended_basket'] = basket
        # add hash to response
        response['user_settings_hash'] = user_settings.pre_user_creation_hash

        response = json.dumps(response)
        return HttpResponse(response, content_type="application/json")


    # get basket for someone who already has an account
    def get_later_basket(self, request, **kwargs):
        user = request.user

        # get the basket and the corresponding recommended_basket id used
        # during the basket porting...
        basket, urb_id = basket_recommendation_engine.get_or_create_later_basket(user)

        if basket:
            response = {}
            response['recommended_basket'] = basket
            response['recommended_basket_id'] = urb_id

            data = json.dumps(response)
            return HttpResponse(data, content_type="application/json")

        else:
            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                                content_type="application/json")

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

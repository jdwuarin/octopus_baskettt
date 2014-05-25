import json

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
import utils
from django.conf import settings

from django.contrib.auth.forms import PasswordResetForm


class UserResource(ModelResource):
    class Meta:
        queryset = OctopusUser.objects.all()
        fields = ['email', 'date_joined']  # we can either whitelist like this or blacklist using exclude
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

            url(r'^(?P<resource_name>%s)/update_settings%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_settings'),
                 name='api_update_settings'),

            url(r'^(?P<resource_name>%s)/settings%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('settings'),
                 name='api_settings'),

            url(r'^(?P<resource_name>%s)/password/done%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('password_done_cb'),
                 name='api_password_reset_complete'),
        ]

    # Get the settings of the user
    def settings(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        response = {}

        if request.user and request.user.is_authenticated():
            user = request.user
            user_settings = UserSettings.objects.get(user=user)
            response["email"] = user.email
            response["recommendation_email_subscription"] = user_settings.recommendation_email_subscription
            response["news_email_subscription"] = user_settings.news_email_subscription
            response["is_private"] = user_settings.is_private

        data = json.dumps(response)
        return HttpResponse(data, content_type="application/json")

    def update_settings(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        email = data.get('email', '')
        recommendation_email_subscription = data.get('recommendation_email_subscription', '')
        news_email_subscription = data.get('news_email_subscription', '')
        is_private = data.get('is_private')

        response = {}

        if not email:
            response["success"] = False
            response["message"] = "Empty email"

        elif request.user and request.user.is_authenticated():
            user = request.user
            user.email = email
            user.username = email

            user_settings = UserSettings.objects.get(user=user)
            user_settings.recommendation_email_subscription = recommendation_email_subscription
            user_settings.news_email_subscription = news_email_subscription
            user_settings.is_private = is_private

            try:
                user.clean()
                user.save()
                user_settings.save()
                response["success"] = True
            except ValidationError:
                response["success"] = False
                response["message"] = "Email address already exists"
        else:
            response["success"] = False
            response["message"] = "User not authenticated"

        data = json.dumps(response)
        return HttpResponse(data, content_type="application/json")

    def password_done_cb(self, request, **kwargs):
        response = {}
        response["status"] = "success"

        data = json.dumps(response)
        return HttpResponse(data, content_type="application/json")

    def password_reset_done_cb(self, request, **kwargs):
        response = {}
        response["status"] = "mail_sent"

        data = json.dumps(response)
        return HttpResponse(data, content_type="application/json")

    def password_reset_confirm_cb(self, request, **kwargs):

        data = {}
        data['password'] = request.POST['new_password1']
        data['password_confirm'] = request.POST['new_password2']
        not_valid = utils.test_password_validation(request, data, self)

        if not_valid:
            return not_valid

        return password_reset_confirm(request,
            post_reset_redirect=utils.get_client_url(request)+'api/v1/user/password/done?format=json',
            uidb64=kwargs["uidb64"],
            token=kwargs["token"])

    def password_reset_cb(self, request, **kwargs):

        return password_reset(request,
            post_reset_redirect=utils.get_client_url(request) + 'api/v1/user/password/reset/done?format=json',
            email_template_name='password_reset_email.html')

    def login(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(email=email.lower(), password=password)

        if user:
            if user.is_active:
                login(request, user)

                return self.create_response(request, {
                    #redirect to a success page
                    'success': True,
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

        not_valid = utils.test_password_validation(request, data, self)

        if not_valid:
            return not_valid


        try:
            # try saving the user
            OctopusUser.objects.create_user(email, password)

        except ValidationError as e:
            try:
                # this is where the custom validation error code is put
                error_type = e.code

                if error_type == "already_exists":
                    return self.create_response(request, {
                        #user with same email address already exists
                        'reason': 'already_exists',
                        'success': False
                    })

            except:
                # some error occured, return success False
                return self.create_response(request, {
                    #some other error occured
                    'reason': 'unidentified_error',
                    'success': False
                })

        # Save settings after registration
        user = authenticate(email=email.lower(), password=password)
        user_settings = utils.save_user_settings(user)
        if not user_settings:
            #remove user that was created without settings
            user.delete()
            return self.create_response(request, {
                #could not find user settings according to hash
                'reason': 'user_settings_not_found',
                'success': False
            })

        # then login the user
        login(request, user)

        # user successfully signed_up
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


    #get basket for someone who has no account yet.
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

            response = json.dumps(response)
            return HttpResponse(response, content_type="application/json")

        else:
            no_success = json.dumps({'success': False})
            return HttpResponse(no_success,
                                content_type="application/json")

from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from octopus_groceries.models import *
from django_hstore import hstore
from octopus_user import managers


class OctopusUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField(default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = managers.OctopusUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password will be prompted for by default

    def clean(self):

        self.validate_unique_email()
        self.validate_user_is_invited()

    def validate_unique_email(self):

        user_exists = OctopusUser.objects.filter(
            email=self.email.lower()).exclude(id=self.id)
        if user_exists:
            raise ValidationError('%s already has an account' % self.email,
                                  code='already_exists')

    def validate_user_is_invited(self):
        try:
            user_invited = UserInvited.objects.get(email=self.email.lower())
            if not user_invited.is_invited:
                # user has already tried signing up but we have
                # not allowed him to use our beta yet. I.e, user is
                # not invited
                raise ValidationError(
                    '%s not accepted as beta user yet' % self.email,
                    code='not_accepted')
            else:
                pass
        except UserInvited.DoesNotExist:
            # user is not yet in the userInvited list
            # we add him with the is_invited flag set to False
            # we return a success false as user could not sign up
            user_invited = UserInvited(email=self.email.lower())
            user_invited.save()
            raise ValidationError(
                '%s not added to beta list yet' % self.email,
                code='not_invited')


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                blank=True, null=True, primary_key=True)

    # email subscription bullshit stuff.
    recommendation_email_subscription = models.BooleanField(default=True)
    next_recommendation_email_date = models.DateField(default=None, blank=True,
                                                      null=True)
    news_email_subscription = models.BooleanField(default=True)
    profile_is_open = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True,
                                      default=datetime.datetime.now())

    def __unicode__(self):
        return "user_settings_of: " + str(self.user)


class UserRelationship(models.Model):
    user_followed = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    user_following = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)


class AvailableTag(models.Model):  # for recipes
    name = models.CharField(max_length=150, default='', editable=False)

    def __unicode__(self):
        return str(self.name)


class UserBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField(blank=True, default='')
    product_dict = hstore.DictionaryField()  # product_id's mapped to quantities
    people = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.name) + ", " + str(
            self.description) + ", " + str(
            self.created_at)


class UserBasketTag(models.Model):
    tag = models.ForeignKey(AvailableTag, blank=False)
    user_basket = models.ForeignKey(UserBasket)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_basket)


class UserCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    name = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField(blank=True, default='')
    basket_list = models.CommaSeparatedIntegerField(max_length=60)
    people = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(),
                                      auto_now=True)

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.name) + ", " + str(
            self.description) + ", " + str(
            self.created_at)


class UserCartTag(models.Model):
    tag = models.ForeignKey(AvailableTag, blank=False)
    user_cart = models.ForeignKey(UserCart)

    def __unicode__(self):
        return str(self.tag) + ", " + str(self.user_cart)


class UserInvited(models.Model):
    email = models.EmailField(max_length=254, editable=True,
                              primary_key=True)
    is_invited = models.NullBooleanField(editable=True, default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                auto_now_add=True)

    def clean(self):
        self.validate_unique_user_invited_email()

    def validate_unique_user_invited_email(self):
        try:
            UserInvited.objects.get(email=self.email.lower())
            # email found, raise error
            raise ValidationError(
                '%s has already subscribed for an invitation' % self.email,
                code='already_subscribed')

        except UserInvited.DoesNotExist:
            pass
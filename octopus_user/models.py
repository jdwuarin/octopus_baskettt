from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from octopus_groceries.models import *
from django_hstore import hstore
from octopus_user import managers


def validate_unique_octopus_user_email(email):

    try:
        OctopusUser.objects.get(email=email.lower())
        # email found, raise error
        raise ValidationError(['already_exist',
              '%s already has an account' % email])

    except OctopusUser.DoesNotExist:
        pass


def validate_user_is_invited(email):
    try:
        user_invited = UserInvited.objects.get(email=email.lower())
        if not user_invited.is_invited:
            # user has already tried signing up but we have
            # not allowed him to use our beta yet. I.e, user is
            # not invited
            raise ValidationError(['not_accepted',
                                  '%s not accepted as beta user yet' % email])
        else:
            pass
    except UserInvited.DoesNotExist:
        # user is not yet in the userInvited list
        # we add him with the is_invited flag set to False
        # we return a success false as user could not sign up
        user_invited = UserInvited(email=email.lower())
        user_invited.clean_fields()
        user_invited.save()
        raise ValidationError(['not_invited',
                              '%s not added to beta list yet' % email])


class OctopusUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True,
                              validators=[validate_unique_octopus_user_email,
                                          validate_user_is_invited])
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


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    people = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    # value from 0 to 1. 0 completely insensitive, 1 extremely sensitive
    price_sensitivity = models.DecimalField(max_digits=10, decimal_places=4)
    tags = models.CommaSeparatedIntegerField(max_length=5000, default=[])
    default_supermarket = models.ForeignKey(
        Supermarket,default=None, blank=True, null=True, editable=False)
    pre_user_creation_hash = models.CharField(
        max_length=150, default='', editable=False, blank=True, null=True,
        db_index=True)

    # email subscription bullshit stuff.
    recommendation_email_subscription = models.BooleanField(default=True)
    next_recommendation_email_date = models.DateField(default=None, blank=True,
                                                      null=True)
    news_email_subscription = models.BooleanField(default=True)

    diet = models.ForeignKey(Diet, blank=True, null=True)
    banned_meats = models.CommaSeparatedIntegerField(
        max_length=5000, default=[])  # id list of BannableMeats
    banned_abstract_products = models.CommaSeparatedIntegerField(
        max_length=5000, default=[])  # id list of AbstractProducts

    created_at = models.DateTimeField(auto_now_add=True,
                                      default=datetime.datetime.now())


    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.people) + ", " + str(
            self.days) + ", " + str(
            self.price_sensitivity) + ", " + str(
            self.tags) + ", " + str(
            self.diet) + ", " + str(
            self.default_supermarket) + ", " + str(
            self.banned_meats) + ", " + str(
            self.banned_abstract_products)


# basket that was recommended to our user by our algorithm
class UserRecommendedBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    product_dict = hstore.DictionaryField()  # product_id's mapped to quantities
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                auto_now_add=True)

    objects = hstore.HStoreManager()


# basket that was finally transferred to the supermarket
# (before items failed being transferred etc)
# saving commaSeperatedValues: user_generated_basket =
class UserGeneratedBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    user_recommended_basket = models.OneToOneField(UserRecommendedBasket,
                                                   primary_key=True)
    product_dict = hstore.DictionaryField()
    created_at = models.DateTimeField(default=datetime.datetime.now(),
                                auto_now_add=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.user) + ", " + str(
            self.user_recommended_basket.id) + ", " + str(
            self.product_dict) + ", " + str(
            self.time)


class UserProductSlack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    product = models.ForeignKey(Product, editable=False)
    slack = models.DecimalField(max_digits=10, decimal_places=4, editable=True)
    purchase_time = models.DateTimeField(default=datetime.datetime.now(),
                                         auto_now_add=True)


def validate_unique_user_invited_email(email):

    try:
        UserInvited.objects.get(email=email.lower())
        # email found, raise error
        raise ValidationError(["already_subscribed",
            '%s has already subscribed for an invitation' % email])

    except UserInvited.DoesNotExist:
        pass


class UserInvited(models.Model):
    email = models.EmailField(max_length=254, editable=True,
                              primary_key=True,
                              validators=[validate_unique_user_invited_email])
    is_invited = models.NullBooleanField(editable=True, default=False)
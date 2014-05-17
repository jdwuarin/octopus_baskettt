from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from octopus_groceries.models import *
from django_hstore import hstore
from django_countries.fields import CountryField
from django_countries import countries
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

    def validate_unique_email(self):

        user_exists = OctopusUser.objects.filter(
            email=self.email.lower()).exclude(id=self.id)
        if user_exists:
            raise ValidationError('%s already has an account' % self.email,
                                  code='already_exists')


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                blank=True, null=True, primary_key=True)

    # email subscription bullshit stuff.
    recommendation_email_subscription = models.BooleanField(default=True)
    next_recommendation_email_date = models.DateField(default=None, blank=True,
                                                      null=True)
    news_email_subscription = models.BooleanField(default=True)
    # allows all users basket to be browsed
    is_private = models.BooleanField(default=False)
    default_supermarket = models.ForeignKey(Supermarket,
                                            default=Supermarket.objects.get(name='tesco'))
    zip_code = models.CharField(max_lenght=100, default='',
                                null=True, blank=True)
    current_country = CountryField(default=dict(countries)['GB']) # use ugettext to get name

    created_at = models.DateTimeField(auto_now_add=True,
                                      default=datetime.datetime.now())

    def __unicode__(self):
        return "user_settings_of: " + str(self.user)


class UserRelationship(models.Model):
    user_followed = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    user_following = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)


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
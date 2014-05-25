from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone


class OctopusUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff,**extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = email.lower() #lower case email field completely
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.clean() #only perform those validations on user creation
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True,
                                 **extra_fields)
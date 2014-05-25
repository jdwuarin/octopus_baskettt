from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory


class TestBase(TestCase):

    fixtures = ['product_fixture.json',]

    def setUp(self):
        self.rf = RequestFactory()
        self.test1 = settings.AUTH_USER_MODEL.objects.create_user(
            email='test1@test.com', password='test')
        self.test1.clean()
        self.test1.save()

        self.test2 = settings.AUTH_USER_MODEL.objects.create_user(
            email='test2@test.com', password='test')
        self.test2.clean()
        self.test2.save()

        self.test2 = settings.AUTH_USER_MODEL.objects.create_user(
            email='test2@test.com', password='test')
        self.test2.clean()
        self.test2.save()
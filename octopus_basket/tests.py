from octopus.test_base import TestBase
from django.core.urlresolvers import reverse

class TestBasket(TestBase):
    def test_creating_basket(self):
        test_url = reverse('api:baskets:baskets')


    def test_deleting_basket(self):
        pass

    def test_porting_basket(self):
        pass

    def test_listing_baskets(self):
        pass

    def test_updating_basket(self):
        pass
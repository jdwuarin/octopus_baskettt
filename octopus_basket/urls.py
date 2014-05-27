from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from octopus_basket import views


# API endpoints
urlpatterns = format_suffix_patterns(patterns('octopus_basket.views',
    url(r'^$', 'api_root'),
    url(r'^baskets/$',
        views.BasketList.as_view(),
        name='basket-list'),
    url(r'^baskets/(?P<pk>[^/]+)/$',
        views.BasketDetail.as_view(),
        name='basket-detail')
))
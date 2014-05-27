from octopus_groceries.api import ProductResource
from octopus_user.api import UserResource
from tastypie.api import Api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
import os
from django.conf import settings


v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(UserResource())

# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'baskets': reverse('basket-list', request=request, format=format),
#     })


api_urls = patterns('',
    url(r'^$', 'api_root'),
    url(r'^', include('octopus_basket.urls', namespace='baskets')),

)

urlpatterns = patterns('',
    url(r'^$', 'octopus_groceries.views.index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^', include('octopus_basket.urls', namespace='baskets')),
    url(r'^api/v2/', include(api_urls, namespace='api')),
    url(r'^port_cart/', 'octopus_basket.views.port_cart'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

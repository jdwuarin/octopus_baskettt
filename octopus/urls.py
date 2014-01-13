from octopus_groceries.api import ProductResource
from octopus_user.api import UserResource
from tastypie.api import Api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
import os
from django.conf import settings


from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^$', 'octopusProducts.views.index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^port_basket/', 'octopus_basket_porting.views.port_basket'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

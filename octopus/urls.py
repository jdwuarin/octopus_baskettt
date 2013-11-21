from octopusProducts.api import ProductResource, UserResource
from tastypie.api import Api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
	url(r'^$', 'octopusProducts.views.index'),
	url(r'^recommendation/', 'octopusProducts.views.recommendation'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += staticfiles_urlpatterns()
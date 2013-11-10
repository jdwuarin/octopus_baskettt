from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *
from tastypie import *
from api import ProductResource

from django.contrib import admin
admin.autodiscover()

v1_api = api.Api(api_name='v1')
v1_api.register(ProductResource())

urlpatterns = patterns('',
	url(r'^$', 'views.index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += staticfiles_urlpatterns()

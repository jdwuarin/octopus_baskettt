from django.conf.urls import patterns, url
from products import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

urlpatterns = patterns('',

    url(r'^$', views.index),
    url(r'^(?P<product_id>\w+)/', views.show),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

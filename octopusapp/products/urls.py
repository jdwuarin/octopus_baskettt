from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',

    url(r'^$', views.index),
    url(r'^(?P<product_id>\w+)/', views.show),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
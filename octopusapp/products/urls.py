from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<product_id>\d+)/$', views.detail, name='detail'),
)
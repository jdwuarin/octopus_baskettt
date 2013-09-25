from django.conf.urls import patterns, url
from rest_framework import routers
from products import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

urlpatterns = patterns('',

    url(r'^$', views.index),
    url(r'^', include(router.urls)),
    url(r'^products/', include('rest_framework.urls', namespace='rest_framework'))
    url(r'^(?P<product_id>\w+)/', views.show),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', 'products.views.index'), # / is the index of the products
    url(r'^products/', include('products.urls')),
)

from django.conf.urls.defaults import *
from api import NotesResource

from tastypie import api

v1_api = api.Api(api_name='v1')
v1_api.register(NotesResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)

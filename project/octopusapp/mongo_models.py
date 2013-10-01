from mongoengine.document import *
from mongoengine.fields import *

class Notes(Document):
    title=StringField(max_length=255)
    text=StringField(max_length=5000)
    
from tastypie_mongoengine import resources


class NotesResource(resources.MongoEngineResource):
    class Meta:
        queryset = Notes.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')    
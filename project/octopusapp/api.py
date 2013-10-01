from tastypie_mongoengine import resources
from products.models import Notes

class NotesResource(resources.MongoEngineResource):
    class Meta:
        queryset = Notes.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')    
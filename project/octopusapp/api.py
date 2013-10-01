#from tastypie.resources import ModelResource

from tastypie_mongoengine import resources
from tastypie.authorization import Authorization
from tastypie_mongoengine import fields
from rest.Document import Filme, Disco
 
class FilmeResource(resources.MongoEngineResource):
    
    class Meta:
        queryset = Filme.objects.all()
        #object_class = Filme
        allowed_methods = ('get', 'post', 'put', 'delete')
        list_allowed_methods = ['get', 'post','put', 'delete']
        authorization = Authorization()
        resource_name = 'Filme'
        #fields = ['Nome', 'Sobrenome']
        #excludes = ['Nome']
    def determine_format(self, request): 
        return "application/json"

class DiscoResource(resources.MongoEngineResource): 
      
    filme = fields.ReferenceField(to='rest.api.FilmeResource',
         attribute='filme', full=True, null=True)
    

    class Meta:
        queryset = Disco.objects.all()
        #object_class = Disco
        allowed_methods = ('get', 'post', 'put', 'delete')
        list_allowed_methods = ['get', 'post','put', 'delete']
        authorization = Authorization()
        resource_name = 'Disco'
    
    def determine_format(self, request): 
        return "application/json"



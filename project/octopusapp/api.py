from tastypie_mongoengine import resources
from products.models import Product

class ProductResource(resources.MongoEngineResource):
    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')

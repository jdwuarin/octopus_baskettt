from tastypie.resources import ModelResource
from products.models import Product

class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')

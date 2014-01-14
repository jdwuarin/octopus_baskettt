from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from models import Product, Recipe
from django.http import HttpResponse
import json


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'product'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_product_search"),
        ]

    # product/search/?format=json&term=query
    def search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)[:10]

        results = []

        data = []
        for product in products:
            product_json = {}
            product_json['id'] = product.id
            product_json['name'] = product.name
            product_json['price'] = product.price
            product_json['img'] = str(product.external_image_link)
            results.append(product_json)
            data = json.dumps(results)

        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']
        resource_name = 'recipe'
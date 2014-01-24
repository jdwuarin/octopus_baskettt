from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from models import Product, Recipe
from django.http import HttpResponse, HttpResponseNotFound
from product_objects_authorization import ProductObjectsAuthorization
import json
from haystack.query import SearchQuerySet

from octopus_groceries.models import AbstractProduct
from octopus_search_engine.octopus_search_engine import perform_search



class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ['get']
        resource_name = 'product'
        authorization = ProductObjectsAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_product_search"),
            url(r"^(?P<resource_name>%s)/autocomplete%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete'), name="api_autocomplete"),
        ]

    # product/search/?format=json&term=query
    def search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        query = request.GET.get('term', '')

        result_products = perform_search(query)

        result_json = []
        for product in result_products:
            product_json = {}
            product_json['id'] = product.id
            product_json['name'] = product.name
            product_json['price'] = product.price
            product_json['link'] = product.link
            product_json['img'] = str(product.external_image_link)
            result_json.append(product_json)

        result_json = json.dumps(result_json)

        mimetype = 'application/json'
        return HttpResponse(result_json, mimetype)

    def autocomplete(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        query = request.GET.get('term', '')

        sqs = SearchQuerySet().autocomplete(
            content_auto=query).models(AbstractProduct)

        data = []
        if sqs:
            for entry in sqs:
                if query in entry.object.name:
                    product_json = {}
                    product_json['name'] = entry.object.name
                    data.append(product_json)

        data = json.dumps(data)

        mimetype = 'application/json'
        return HttpResponse(data, mimetype)



class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']
        resource_name = 'recipe'
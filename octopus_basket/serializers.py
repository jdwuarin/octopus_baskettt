from rest_framework import serializers
from django.db import models
from django.conf import settings
from octopus_groceries.models import Product
from octopus_basket.models import Basket
import random
import string


class ProductDictField(serializers.WritableField):

    def to_native(self, obj):
        # object to primitives (essentially what I have in the db
        # to what I send to the client)
        product_list = []
        for product_id in obj.product_dict.iteritems():
            product_info = {}
            product = Product.objects.get(id=int(product_id))
            product_info['id'] = product_id
            product_info['name'] = product.name
            product_info['price'] = product.price
            product_info['link'] = product.link
            product_info['img'] = str(product.external_image_link)

            if product.department:
                product_info['department'] = product.department.name

            product_list.append(product_info)

        return product_list

    def from_native(self, obj):
        product_dict = {}
        for product in obj.product_dict:
            product_id = product.product_id
            query_term = product.query_term
            quantity = product.quantity
            product_dict[product_id] = [query_term, quantity]

        return product_dict


class BasketSerializer(serializers.Serializer):
    user = serializers.Field(source='user.id')
    name = serializers.CharField(max_length=250)
    parent = serializers.Field(source='parent.hash')
    description = serializers.CharField(required=False)
    product_dict = ProductDictField()
    hash = serializers.CharField(max_length=60, required=False)
    is_public = serializers.BooleanField()
    is_browsable = serializers.BooleanField()
    ordering_fields = ('name',)
    ordering = 'name'

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.name = attrs['name']
            instance.description = attrs['description']
            instance.product_dict = attrs['product_dict']
            instance.content = attrs.get('content', instance.content)
            instance.created = attrs.get('created', instance.created)
            return instance

        attrs['user'] = settings.AUTH_USER_MODEL.objetcs.get(id=attrs['user'])
        attrs['parent'] = Basket.objects.get(hash=attrs['parent'])
        attrs['hash'] = ''.join(random.choice(
            string.ascii_letters + string.digits) for x in range(22))

        return Basket(**attrs)
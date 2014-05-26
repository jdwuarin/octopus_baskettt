from rest_framework import serializers
from django.db import models
from django.conf import settings
from octopus_groceries.models import Product
from octopus_basket.models import Basket
from octopus_user.models import OctopusUser
import random
import string
import ast


class ProductDictField(serializers.WritableField):

    def to_native(self, obj):
        # object to primitives (essentially what I have in the db
        # to what I send to the client)
        product_list = []
        for product_id, __ in obj.iteritems():
            product_info = {}
            product = Product.objects.get(id=int(product_id))
            product_info['id'] = product_id
            product_info['name'] = product.name
            product_info['price'] = product.price
            product_info['link'] = product.link
            product_info['img'] = str(product.external_image_link)
            product_info['quantity'] = ast.literal_eval(obj[product_id])[1]

            if product.department:
                product_info['department'] = product.department.name

            product_list.append(product_info)

        return product_list

    def from_native(self, obj):
        product_dict = {}

        for product in obj:
            product_id = product['id']
            query_term = product['query_term']
            quantity = product['quantity']
            product_dict[str(product_id)] = str([query_term, quantity])

        return product_dict


class BasketSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    parent = serializers.Field(source='parent.hash')
    description = serializers.CharField(required=False)
    product_dict = ProductDictField()
    hash = serializers.CharField(max_length=60, required=False)
    is_public = serializers.BooleanField()
    is_browsable = serializers.BooleanField()
    ordering_fields = ('name',)
    ordering = 'name'

    # def from_native(self, data, files=None):
    #     """
    #     Deserialize primitives -> objects.
    #     """
    #     self._errors = {}
    #
    #     if data is not None or files is not None:
    #         attrs = self.restore_fields(data, files)
    #         if attrs is not None:
    #             attrs = self.perform_validation(attrs)
    #     else:
    #         self._errors['non_field_errors'] = ['No input provided']
    #
    #     if not self._errors:
    #         return self.restore_object(attrs, instance=getattr(self, 'object', None))


    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """

        print attrs
        if instance is not None:
            instance.name = attrs['name']
            instance.description = attrs['description']
            instance.product_dict = attrs['product_dict']
            instance.content = attrs.get('content', instance.content)
            instance.created = attrs.get('created', instance.created)
            return instance

        #attrs['user'] = OctopusUser.objects.get(id=attrs['user'])
        try:
            attrs['parent'] = Basket.objects.get(hash=attrs['parent'])
        except KeyError:
            pass

        attrs['hash'] = ''.join(random.choice(
            string.ascii_letters + string.digits) for x in range(22))

        return Basket(**attrs)

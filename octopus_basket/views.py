import json
from django.http import HttpResponse
from octopus_basket.basket_to_port import BasketToPort
from octopus_basket.spider_manager import SpiderManagerController
from octopus_basket.thread_manager import ThreadManager
from django.contrib.auth.decorators import login_required
from octopus_groceries.models import Product, Tag
from octopus_user.models import UserSettings
from octopus_basket.pipelines import BadLoginException
import octopus_recommendation_engine.helpers
import utils
from rest_framework import generics, permissions
from octopus_basket.models import Basket, Cart
from octopus_basket.serializers import BasketSerializer
from octopus_basket.permissions import IsOwner, IsOwnerOrPublic


class BasketList(generics.ListCreateAPIView):
    serializer_class = BasketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwner, )

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = Basket.objects.filter(user=self.request.user)
        return queryset


class BasketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrPublic, )

    def pre_save(self, obj):
        obj.user = self.request.user


@login_required
def port_cart(request):
    SpiderManagerController.create_if_none()
    data = json.loads(request.body)

    # first determine what user made this request
    user = request.user

    email = data['email']
    password = data['password']
    product_list_before_porting = []

    # for now, I get a list of basket ids. Later, I will
    # just get a cart Id and extrapolate from there

    basket_ids = data['basket_ids']
    baskets = Basket.objects.get(id__in=basket_ids)
    for basket in baskets:
        # check if owner:
        if not IsOwner().has_object_permission(request, None, basket):
            res = {}
            res['success'] = False
            return HttpResponse(json.dumps('res'),
                                content_type="application/json")

        for product_id in basket.product_dict.iteritems():
            quantity = str(int(basket.product_dict['product_id'][0]))
            product_list_before_porting.append(
                Product.objects.get(id=product_id), quantity)


    thread_manager = ThreadManager()
    this_basket = BasketToPort(request, email, password,
                               product_list_before_porting,
                               thread_manager)

    SpiderManagerController.add_basket_to_port(this_basket)

    this_basket.thread_manager.wait(20)

    product_list_after_porting = this_basket.thread_manager.get_response()

    # make sure user could login to tesco. if not, notify user.
    if product_list_after_porting['server_timeout'] =='True' or \
                    product_list_after_porting['good_login'] == "False":
        return HttpResponse(json.dumps(
            product_list_after_porting), content_type="application/json")

    product_list_after_porting = check_basket_persistence(
        product_list_before_porting,
        product_list_after_porting)

    response = {}
    response_product_list = []

    # key[0] is the Product item or a string and. If product item, key[1]
    # is the quantity to order
    for key, is_success in product_list_after_porting.iteritems():
        product_json = dict()
        if not type(key) == str:
            product_json['id'] = key[0].id
            product_json['name'] = key[0].name
            product_json['price'] = key[0].price
            product_json['link'] = key[0].link
            product_json['img'] = str(key[0].external_image_link)
            product_json['quantity'] = key[1]
            product_json['success'] = is_success
            response_product_list.append(product_json)

        else:
            # the server status and good_login status
            response[key] = is_success

    # the product list
    response['product_list'] = response_product_list

    # only increment basket purchase_count after porting it

    for basket in baskets:
        basket.purchase_count += 1
        basket.save()

    # frontend needs to check for "Response_status" == "server_timeout" and
    # "good_login" == "False" in that order before anything else
    return HttpResponse(json.dumps(response), content_type="application/json")


def check_basket_persistence(product_list_before, product_list_after):
    #if any item that should be in the product_list_before isn't for some reason,
    #report it here
    for product in product_list_before:
        try:
            dummy = product_list_after[product]
        except KeyError:
            product_list_after[product] = "False"

    return product_list_after

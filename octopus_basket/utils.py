# import json
# from octopus_basket.models import *


# def save_cart(json_cart, user):

#     try:
#         old_cart = UserCart.objects.get(user=user, name=json_cart['name'])
#         success_status = update_cart(old_cart, json_cart)
#     except UserCart.DoesNotExist:
#         success_status = create_cart(json_cart, user)

#     return success_status


# def create_cart(json_cart, user):
#     #first create all baskets
#     basket_list = []
#     for basket in json_cart['basket_list']:
#         saved_basket = save_basket(basket, user)
#         if saved_basket:
#             basket_list.append(saved_basket)
#         else:
#             return False

#     user_cart = UserCart(user=user,
#                          name=json_cart['name'],
#                          parend_id=json_cart['parent_id'],
#                          description=json_cart['description'],
#                          basket_list=basket_list)
#     user_cart.save()

#     return True


# def update_cart(old_cart, json_cart):

#     json_basket_list = json_cart['basket_list']


#     pass


# def save_basket(basket, user):
#     try:
#         old_basket = UserBasket.objects.get(user=user, name=basket['name'])
#         success_status = update_cart(old_cart, cart)
#     except UserCart.DoesNotExist:
#         success_status = create_cart(cart, user)

#     return success_status


# def create_basket(request):
#     pass


# def get_cart(request):
#     pass


# def get_basket(request):
#     pass
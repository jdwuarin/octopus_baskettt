from django.shortcuts import render
from django.http import Http404

from products.models import Product

def index(request):
	latest_products = Product.objects
	context = {'latest_products': latest_products}
	return render(request, 'products/index.html', context)
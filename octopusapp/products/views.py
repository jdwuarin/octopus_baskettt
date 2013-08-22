from django.shortcuts import render,get_object_or_404

from products.models import Product


def index(request):
	latest_products = Product.objects
	context = {'latest_products': latest_products}
	return render(request, 'products/index.html', context)

def show(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request, 'products/show.html', {'product': product})
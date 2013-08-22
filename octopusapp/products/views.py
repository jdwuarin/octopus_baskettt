from django.shortcuts import render
from django.http import Http404

from products.models import Product


def index(request):
	latest_products = Product.objects
	context = {'latest_products': latest_products}
	return render(request, 'products/index.html', context)

def show(request, product_id):
	product = get_obj_or_404(Product, pk=product_id)
	return render(request, 'products/show.html', {'product': product})


# Because we have a mongoengine model and not a Django, we have to redefine the function
def get_obj_or_404(klass, *args, **kwargs): 
	try:									
		return klass.objects.get(*args, **kwargs)
	except klass.DoesNotExist:
		raise Http404
from django.http import HttpResponse
from django.template import RequestContext, loader

from products.models import Product


def index(request):
	latest_products = Product.objects.all
	template = loader.get_template('products/index.html')
	context = RequestContext(request, {
        'latest_products': latest_products,
    })
	return HttpResponse(template.render(context))

def detail(request, product_id):
    return HttpResponse("You're looking at product %s." % product_id)
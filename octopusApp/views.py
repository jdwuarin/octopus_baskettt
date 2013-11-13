from django.shortcuts import render
from api import ProductResource
from django.http import HttpResponse


def index(request):
	return render(request, 'products/index.html')

def recommendation(request):
	print request.method

	print "//////"
	print request.body
	print "//////"

	res = ProductResource()
	request_bundle = res.build_bundle(request=request)
	queryset = res.obj_get_list(request_bundle)
	response = HttpResponse(queryset, content_type="text/json")
	return response
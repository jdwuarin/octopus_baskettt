from django.shortcuts import render
from django.conf import settings


def index(request):
    context = {'debug': settings.DEBUG}
    if settings.DEBUG:
        return render(request, 'products/index_dev.html', context)
    else:
        return render(request, 'products/index_prod.html', context)




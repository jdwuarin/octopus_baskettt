from django.shortcuts import render
from django.conf import settings

def index(request):

    if request.user.is_authenticated():
        email = str(request.user.email)
    else:
        email = ""

    context = {'debug': settings.DEBUG, 'email': email}

    if settings.DEBUG:
        return render(request, 'products/index_dev.html', context)
    else:
        return render(request, 'products/index_prod.html', context)

from django.contrib import admin
from models import Product

# class ProductAdmin(admin.ModelAdmin):
#     fields = ['price', 'link']

admin.site.register(Product)
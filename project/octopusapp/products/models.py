from django.db import models

class Product(models.Model):
    title=models.CharField(max_length=50)
    text=models.CharField(max_length=50)
    

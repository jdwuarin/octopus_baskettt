from django.db import models

class Product(models.Model):

    #added price, productOrigin, image etc
    price=models.CharField(max_length=12, default='NaN', editable=False)
    productOrigin=models.CharField(max_length=50, default='none', editable=False)
    #max_length is defaulted to 100 for image.
    image=models.ImageField(upload_to="images/" + str(productOrigin) + "/", default='', editable=False)
    name=models.CharField(max_length=150, default='', editable=False)
    link=models.CharField(max_length=200, default='', editable=False)
    description=models.CharField(max_length=300, default='')
    offer_flag=models.CharField(max_length=12, default=False, editable=False)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.price) + ", " + str(self.productOrigin)

    #might be able to remove default "title" and "text" entries at some point

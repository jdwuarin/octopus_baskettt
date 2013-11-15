from django.db import models

class Product(models.Model):
    title=models.CharField(max_length=50)
    text=models.CharField(max_length=50)


    #added price, productOrigin, image etc
    price=models.CharField(max_length=12)
    productOrigin=models.CharField(max_length=50)
    #max_length is defaulted to 100 for image.
    image=models.ImageField(upload_to="images/" + str(productOrigin) + "/")
    name=models.CharField(max_length=150)
    link=models.CharField(max_length=200)
    description=models.CharField(max_length=300)

    def __unicode__(self):  # just adding this method to say what to display when asked in shell
        return str(self.name) + ", " + str(self.price) + ", " + str(self.productOrigin)

    #might be able to remove default "title" and "text" entries at some point

from mongoengine.document import *
from mongoengine.fields import *

class Product(Document):
    name=StringField(max_length=255)
    text=StringField(max_length=5000)
    

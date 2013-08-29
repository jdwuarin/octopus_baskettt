from mongoengine import *

class Product(Document):
    name = StringField(max_length=200)
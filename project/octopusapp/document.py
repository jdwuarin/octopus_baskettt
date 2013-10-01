from mongoengine import *
from Apli.settings import DBName


connect(DBName)

import mongoengine

from mongoengine import Document, fields

class Filme(mongoengine.Document):
    TituloOriginal = StringField(max_length=100, required=True)
    TituloPT = StringField(max_length=100, required=True)
    Genero = StringField(max_length=50, required=True)
    Classificacao = DecimalField()
    Ano = IntField()
    Duracao = StringField(max_length=120, required=True)
    Observacoes = StringField(max_length=120, required=True)
    Capa = StringField()


class Disco(mongoengine.Document):
    Tipo = StringField(max_length=100, required=True)
    Legendas = StringField(max_length=100, required=True)
    OndeComprado = StringField(max_length=100, required=True)
    Observacoes = StringField(max_length=100, required=True)
    
    filme = ReferenceField(Filme,
                        reverse_delete_rule=CASCADE, dbref=False)
    


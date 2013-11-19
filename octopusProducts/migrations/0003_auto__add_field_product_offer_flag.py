# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.offer_flag'
        db.add_column(u'octopusProducts_product', 'offer_flag',
                      self.gf('django.db.models.fields.CharField')(default=False, max_length=12),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.offer_flag'
        db.delete_column(u'octopusProducts_product', 'offer_flag')


    models = {
        u'octopusProducts.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'offer_flag': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '12'}),
            'price': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '12'}),
            'productOrigin': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['octopusProducts']
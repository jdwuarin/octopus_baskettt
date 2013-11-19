# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.offer_flag'
        db.delete_column(u'octopusProducts_product', 'offer_flag')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Product.offer_flag'
        raise RuntimeError("Cannot reverse this migration. 'Product.offer_flag' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Product.offer_flag'
        db.add_column(u'octopusProducts_product', 'offer_flag',
                      self.gf('django.db.models.fields.BooleanField')(),
                      keep_default=False)


    models = {
        u'octopusProducts.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'productOrigin': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['octopusProducts']
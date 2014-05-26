# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Cart.parent'
        db.alter_column(u'octopus_basket_cart', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.Cart'], null=True))

        # Changing field 'Basket.parent'
        db.alter_column(u'octopus_basket_basket', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.Basket'], null=True))

    def backwards(self, orm):

        # Changing field 'Cart.parent'
        db.alter_column(u'octopus_basket_cart', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['octopus_basket.Cart']))

        # Changing field 'Basket.parent'
        db.alter_column(u'octopus_basket_basket', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['octopus_basket.Basket']))

    models = {
        u'octopus_basket.availabletag': {
            'Meta': {'object_name': 'AvailableTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_basket.basket': {
            'Meta': {'object_name': 'Basket'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 26, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '60', 'primary_key': 'True', 'db_index': 'True'}),
            'is_browsable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_basket.Basket']", 'null': 'True', 'blank': 'True'}),
            'product_dict': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'purchase_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 26, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_user.OctopusUser']"})
        },
        u'octopus_basket.baskettag': {
            'Meta': {'object_name': 'BasketTag'},
            'basket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_basket.Basket']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_basket.AvailableTag']"})
        },
        u'octopus_basket.cart': {
            'Meta': {'object_name': 'Cart'},
            'basket_list': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '60'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 26, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '60', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_basket.Cart']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 26, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_user.OctopusUser']"})
        },
        u'octopus_basket.usercarttag': {
            'Meta': {'object_name': 'UserCartTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_basket.AvailableTag']"}),
            'user_cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_basket.Cart']"})
        },
        u'octopus_user.octopususer': {
            'Meta': {'object_name': 'OctopusUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['octopus_basket']
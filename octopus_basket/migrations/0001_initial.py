# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AvailableTag'
        db.create_table(u'octopus_basket_availabletag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopus_basket', ['AvailableTag'])

        # Adding model 'Basket'
        db.create_table(u'octopus_basket_basket', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_user.OctopusUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_basket.Basket'], blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('product_dict', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(default=None, max_length=60, primary_key=True, db_index=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_browsable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('purchase_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 22, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 22, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'octopus_basket', ['Basket'])

        # Adding model 'BasketTag'
        db.create_table(u'octopus_basket_baskettag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.AvailableTag'])),
            ('basket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.Basket'])),
        ))
        db.send_create_signal(u'octopus_basket', ['BasketTag'])

        # Adding model 'Cart'
        db.create_table(u'octopus_basket_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_user.OctopusUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_basket.Cart'], blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('basket_list', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=60)),
            ('hash', self.gf('django.db.models.fields.CharField')(default=None, max_length=60, db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 22, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 22, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'octopus_basket', ['Cart'])

        # Adding model 'UserCartTag'
        db.create_table(u'octopus_basket_usercarttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.AvailableTag'])),
            ('user_cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_basket.Cart'])),
        ))
        db.send_create_signal(u'octopus_basket', ['UserCartTag'])


    def backwards(self, orm):
        # Deleting model 'AvailableTag'
        db.delete_table(u'octopus_basket_availabletag')

        # Deleting model 'Basket'
        db.delete_table(u'octopus_basket_basket')

        # Deleting model 'BasketTag'
        db.delete_table(u'octopus_basket_baskettag')

        # Deleting model 'Cart'
        db.delete_table(u'octopus_basket_cart')

        # Deleting model 'UserCartTag'
        db.delete_table(u'octopus_basket_usercarttag')


    models = {
        u'octopus_basket.availabletag': {
            'Meta': {'object_name': 'AvailableTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_basket.basket': {
            'Meta': {'object_name': 'Basket'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '60', 'primary_key': 'True', 'db_index': 'True'}),
            'is_browsable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_basket.Basket']", 'blank': 'True'}),
            'product_dict': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'purchase_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '60', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_basket.Cart']", 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
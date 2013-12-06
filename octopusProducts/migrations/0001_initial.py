# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'octopusProducts_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.CharField')(default='NaN', max_length=12)),
            ('price_per_unit', self.gf('django.db.models.fields.CharField')(default='NaN', max_length=50)),
            ('product_origin', self.gf('django.db.models.fields.CharField')(default='none', max_length=50)),
            ('external_image_link', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('offer_flag', self.gf('django.db.models.fields.CharField')(default=False, max_length=12)),
            ('external_id', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Product'])

        # Adding model 'Cuisine'
        db.create_table(u'octopusProducts_cuisine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Cuisine'])

        # Adding model 'Consideration'
        db.create_table(u'octopusProducts_consideration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Consideration'])

        # Adding model 'Main_ingredient'
        db.create_table(u'octopusProducts_main_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Main_ingredient'])

        # Adding model 'Recipe'
        db.create_table(u'octopusProducts_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=4)),
            ('review_count', self.gf('django.db.models.fields.IntegerField')()),
            ('external_id', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('main_ingredient', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Main_ingredient'])),
            ('course', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('cuisine', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Cuisine'])),
            ('consideration', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Recipe'])

        # Adding model 'Ingredient'
        db.create_table(u'octopusProducts_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Ingredient'])

        # Adding model 'Recipe_ingredient'
        db.create_table(u'octopusProducts_recipe_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Recipe'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Ingredient'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Recipe_ingredient'])

        # Adding model 'Ingredient_product'
        db.create_table(u'octopusProducts_ingredient_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Ingredient'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('product_tesco', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_tesco_id', to=orm['octopusProducts.Product'])),
        ))
        db.send_create_signal(u'octopusProducts', ['Ingredient_product'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'octopusProducts_product')

        # Deleting model 'Cuisine'
        db.delete_table(u'octopusProducts_cuisine')

        # Deleting model 'Consideration'
        db.delete_table(u'octopusProducts_consideration')

        # Deleting model 'Main_ingredient'
        db.delete_table(u'octopusProducts_main_ingredient')

        # Deleting model 'Recipe'
        db.delete_table(u'octopusProducts_recipe')

        # Deleting model 'Ingredient'
        db.delete_table(u'octopusProducts_ingredient')

        # Deleting model 'Recipe_ingredient'
        db.delete_table(u'octopusProducts_recipe_ingredient')

        # Deleting model 'Ingredient_product'
        db.delete_table(u'octopusProducts_ingredient_product')


    models = {
        u'octopusProducts.consideration': {
            'Meta': {'object_name': 'Consideration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.cuisine': {
            'Meta': {'object_name': 'Cuisine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.ingredient_product': {
            'Meta': {'object_name': 'Ingredient_product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Ingredient']"}),
            'product_tesco': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_tesco_id'", 'to': u"orm['octopusProducts.Product']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {})
        },
        u'octopusProducts.main_ingredient': {
            'Meta': {'object_name': 'Main_ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'external_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'external_image_link': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'offer_flag': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '12'}),
            'price': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '12'}),
            'price_per_unit': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '50'}),
            'product_origin': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'})
        },
        u'octopusProducts.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'consideration': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'course': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'cuisine': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Cuisine']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Main_ingredient']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'octopusProducts.recipe_ingredient': {
            'Meta': {'object_name': 'Recipe_ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Ingredient']"}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Recipe']"})
        }
    }

    complete_apps = ['octopusProducts']
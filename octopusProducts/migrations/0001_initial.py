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

        # Adding model 'Recipe'
        db.create_table(u'octopusProducts_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=4)),
            ('review_count', self.gf('django.db.models.fields.IntegerField')()),
            ('ingredient_list', self.gf('django.db.models.fields.CharField')(max_length=10000)),
        ))
        db.send_create_signal(u'octopusProducts', ['Recipe'])

        # Adding model 'Ingredient'
        db.create_table(u'octopusProducts_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Ingredient'])

        # Adding model 'RecipeIngredient'
        db.create_table(u'octopusProducts_recipeingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopusProducts.Recipe'])),
            ('ingredient_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopusProducts.Ingredient'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'octopusProducts', ['RecipeIngredient'])

        # Adding model 'IngredientProduct'
        db.create_table(u'octopusProducts_ingredientproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopusProducts.Ingredient'])),
            ('product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopusProducts.Product'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'octopusProducts', ['IngredientProduct'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'octopusProducts_product')

        # Deleting model 'Recipe'
        db.delete_table(u'octopusProducts_recipe')

        # Deleting model 'Ingredient'
        db.delete_table(u'octopusProducts_ingredient')

        # Deleting model 'RecipeIngredient'
        db.delete_table(u'octopusProducts_recipeingredient')

        # Deleting model 'IngredientProduct'
        db.delete_table(u'octopusProducts_ingredientproduct')


    models = {
        u'octopusProducts.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.ingredientproduct': {
            'Meta': {'object_name': 'IngredientProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopusProducts.Ingredient']"}),
            'product_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopusProducts.Product']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient_list': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'octopusProducts.recipeingredient': {
            'Meta': {'object_name': 'RecipeIngredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopusProducts.Ingredient']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'recipe_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopusProducts.Recipe']"})
        }
    }

    complete_apps = ['octopusProducts']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.created_at'
        db.add_column(u'octopus_groceries_product', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 22, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.updated_at'
        db.add_column(u'octopus_groceries_product', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 22, 0, 0), auto_now=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.created_at'
        db.delete_column(u'octopus_groceries_product', 'created_at')

        # Deleting field 'Product.updated_at'
        db.delete_column(u'octopus_groceries_product', 'updated_at')


    models = {
        u'octopus_groceries.abstractproduct': {
            'Meta': {'object_name': 'AbstractProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_condiment': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_food': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_groceries.abstractproductsupermarketproduct': {
            'Meta': {'object_name': 'AbstractProductSupermarketProduct'},
            'abstract_product': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.AbstractProduct']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_dict': ('django_hstore.fields.ReferencesField', [], {'db_index': 'True'}),
            'supermarket': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.Supermarket']"})
        },
        u'octopus_groceries.aisle': {
            'Meta': {'object_name': 'Aisle'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Department']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'supermarket_names': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'})
        },
        u'octopus_groceries.bannablemeats': {
            'Meta': {'object_name': 'BannableMeats'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'})
        },
        u'octopus_groceries.category': {
            'Meta': {'object_name': 'Category'},
            'aisle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Aisle']", 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Department']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'supermarket_names': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'})
        },
        u'octopus_groceries.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'supermarket_names': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'})
        },
        u'octopus_groceries.diet': {
            'Meta': {'object_name': 'Diet'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'})
        },
        u'octopus_groceries.nutritionalfacts': {
            'Meta': {'object_name': 'NutritionalFacts'},
            'carbohydrates': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'energy': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'fat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'fibre': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'monounsaturates': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'polyunsaturates': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['octopus_groceries.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'protein': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'salt': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'saturates': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'sodium': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'starch': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'sugar': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'})
        },
        u'octopus_groceries.product': {
            'Meta': {'object_name': 'Product'},
            'aisle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Aisle']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'external_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'external_image_link': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stock': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'price': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '12'}),
            'product_life_expectancy': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'promotion_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'promotion_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '50'}),
            'supermarket': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Supermarket']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'octopus_groceries.recipe': {
            'Meta': {'object_name': 'Recipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'octopus_groceries.recipeabstractproduct': {
            'Meta': {'object_name': 'RecipeAbstractProduct'},
            'abstract_product': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.AbstractProduct']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.Recipe']"}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_groceries.supermarket': {
            'Meta': {'object_name': 'Supermarket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_groceries.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopus_groceries.tagrecipe': {
            'Meta': {'object_name': 'TagRecipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.Recipe']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['octopus_groceries.Tag']"})
        }
    }

    complete_apps = ['octopus_groceries']
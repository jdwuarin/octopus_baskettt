# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supermarket'
        db.create_table(u'octopus_groceries_supermarket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Supermarket'])

        # Adding model 'Department'
        db.create_table(u'octopus_groceries_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('supermarket_names', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Department'])

        # Adding model 'Aisle'
        db.create_table(u'octopus_groceries_aisle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Department'], null=True, blank=True)),
            ('supermarket_names', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Aisle'])

        # Adding model 'Category'
        db.create_table(u'octopus_groceries_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Department'], null=True, blank=True)),
            ('aisle', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Aisle'], null=True, blank=True)),
            ('supermarket_names', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Category'])

        # Adding model 'Product'
        db.create_table(u'octopus_groceries_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supermarket', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Supermarket'], null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Department'], null=True, blank=True)),
            ('aisle', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Aisle'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['octopus_groceries.Category'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.CharField')(default='NaN', max_length=12)),
            ('quantity', self.gf('django.db.models.fields.CharField')(default='NaN', max_length=50)),
            ('product_life_expectancy', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='none', max_length=50)),
            ('external_image_link', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('promotion_flag', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('promotion_description', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('external_id', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(default='')),
            ('in_stock', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 24, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 24, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Product'])

        # Adding model 'NutritionalFacts'
        db.create_table(u'octopus_groceries_nutritionalfacts', (
            ('product', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['octopus_groceries.Product'], unique=True, primary_key=True)),
            ('energy', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('protein', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('carbohydrates', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('sugar', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('starch', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('fat', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('saturates', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('monounsaturates', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('polyunsaturates', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('fibre', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('salt', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('sodium', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
        ))
        db.send_create_signal(u'octopus_groceries', ['NutritionalFacts'])

        # Adding model 'Tag'
        db.create_table(u'octopus_groceries_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Tag'])

        # Adding model 'Recipe'
        db.create_table(u'octopus_groceries_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('review_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'octopus_groceries', ['Recipe'])

        # Adding model 'TagRecipe'
        db.create_table(u'octopus_groceries_tagrecipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.Tag'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.Recipe'])),
        ))
        db.send_create_signal(u'octopus_groceries', ['TagRecipe'])

        # Adding model 'AbstractProduct'
        db.create_table(u'octopus_groceries_abstractproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('is_food', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_condiment', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['AbstractProduct'])

        # Adding model 'RecipeAbstractProduct'
        db.create_table(u'octopus_groceries_recipeabstractproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.Recipe'])),
            ('abstract_product', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.AbstractProduct'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopus_groceries', ['RecipeAbstractProduct'])

        # Adding model 'AbstractProductSupermarketProduct'
        db.create_table(u'octopus_groceries_abstractproductsupermarketproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abstract_product', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.AbstractProduct'])),
            ('supermarket', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['octopus_groceries.Supermarket'])),
            ('product_dict', self.gf('django_hstore.fields.ReferencesField')(db_index=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['AbstractProductSupermarketProduct'])

        # Adding model 'BannableMeats'
        db.create_table(u'octopus_groceries_bannablemeats', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, primary_key=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['BannableMeats'])

        # Adding model 'Diet'
        db.create_table(u'octopus_groceries_diet', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, primary_key=True)),
        ))
        db.send_create_signal(u'octopus_groceries', ['Diet'])


    def backwards(self, orm):
        # Deleting model 'Supermarket'
        db.delete_table(u'octopus_groceries_supermarket')

        # Deleting model 'Department'
        db.delete_table(u'octopus_groceries_department')

        # Deleting model 'Aisle'
        db.delete_table(u'octopus_groceries_aisle')

        # Deleting model 'Category'
        db.delete_table(u'octopus_groceries_category')

        # Deleting model 'Product'
        db.delete_table(u'octopus_groceries_product')

        # Deleting model 'NutritionalFacts'
        db.delete_table(u'octopus_groceries_nutritionalfacts')

        # Deleting model 'Tag'
        db.delete_table(u'octopus_groceries_tag')

        # Deleting model 'Recipe'
        db.delete_table(u'octopus_groceries_recipe')

        # Deleting model 'TagRecipe'
        db.delete_table(u'octopus_groceries_tagrecipe')

        # Deleting model 'AbstractProduct'
        db.delete_table(u'octopus_groceries_abstractproduct')

        # Deleting model 'RecipeAbstractProduct'
        db.delete_table(u'octopus_groceries_recipeabstractproduct')

        # Deleting model 'AbstractProductSupermarketProduct'
        db.delete_table(u'octopus_groceries_abstractproductsupermarketproduct')

        # Deleting model 'BannableMeats'
        db.delete_table(u'octopus_groceries_bannablemeats')

        # Deleting model 'Diet'
        db.delete_table(u'octopus_groceries_diet')


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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 24, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
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
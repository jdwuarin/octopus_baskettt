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
            ('quantity', self.gf('django.db.models.fields.CharField')(default='NaN', max_length=50)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='none', max_length=50)),
            ('product_origin', self.gf('django.db.models.fields.CharField')(default='none', max_length=50)),
            ('external_image_link', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('offer_flag', self.gf('django.db.models.fields.CharField')(default=False, max_length=12)),
            ('external_id', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Product'])

        # Adding model 'Tag'
        db.create_table(u'octopusProducts_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'octopusProducts', ['Tag'])

        # Adding model 'Recipe'
        db.create_table(u'octopusProducts_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('review_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'octopusProducts', ['Recipe'])

        # Adding model 'Tag_recipe'
        db.create_table(u'octopusProducts_tag_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Tag'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Recipe'])),
        ))
        db.send_create_signal(u'octopusProducts', ['Tag_recipe'])

        # Adding model 'Ingredient'
        db.create_table(u'octopusProducts_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('is_condiment', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'octopusProducts', ['Ingredient'])

        # Adding model 'Recipe_ingredient'
        db.create_table(u'octopusProducts_recipe_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Recipe'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Ingredient'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
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

        # Adding model 'User_product_slack'
        db.create_table(u'octopusProducts_user_product_slack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['auth.User'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Ingredient'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['octopusProducts.Product'])),
            ('slack', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('purchase_time', self.gf('django.db.models.fields.DateField')(default=0)),
        ))
        db.send_create_signal(u'octopusProducts', ['User_product_slack'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'octopusProducts_product')

        # Deleting model 'Tag'
        db.delete_table(u'octopusProducts_tag')

        # Deleting model 'Recipe'
        db.delete_table(u'octopusProducts_recipe')

        # Deleting model 'Tag_recipe'
        db.delete_table(u'octopusProducts_tag_recipe')

        # Deleting model 'Ingredient'
        db.delete_table(u'octopusProducts_ingredient')

        # Deleting model 'Recipe_ingredient'
        db.delete_table(u'octopusProducts_recipe_ingredient')

        # Deleting model 'Ingredient_product'
        db.delete_table(u'octopusProducts_ingredient_product')

        # Deleting model 'User_product_slack'
        db.delete_table(u'octopusProducts_user_product_slack')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'octopusProducts.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_condiment': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.ingredient_product': {
            'Meta': {'object_name': 'Ingredient_product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Ingredient']"}),
            'product_tesco': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_tesco_id'", 'to': u"orm['octopusProducts.Product']"}),
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
            'product_origin': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "'NaN'", 'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'})
        },
        u'octopusProducts.recipe': {
            'Meta': {'object_name': 'Recipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'octopusProducts.recipe_ingredient': {
            'Meta': {'object_name': 'Recipe_ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Ingredient']"}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Recipe']"}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'octopusProducts.tag_recipe': {
            'Meta': {'object_name': 'Tag_recipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Recipe']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Tag']"})
        },
        u'octopusProducts.user_product_slack': {
            'Meta': {'object_name': 'User_product_slack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Ingredient']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['octopusProducts.Product']"}),
            'purchase_time': ('django.db.models.fields.DateField', [], {'default': '0'}),
            'slack': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['octopusProducts']
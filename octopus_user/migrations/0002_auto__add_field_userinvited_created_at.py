# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserInvited.created_at'
        db.add_column(u'octopus_user_userinvited', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 28, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserInvited.created_at'
        db.delete_column(u'octopus_user_userinvited', 'created_at')


    models = {
        u'octopus_groceries.aisle': {
            'Meta': {'object_name': 'Aisle'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Department']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'supermarket_names': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'})
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
        u'octopus_groceries.product': {
            'Meta': {'object_name': 'Product'},
            'aisle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Aisle']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'octopus_groceries.supermarket': {
            'Meta': {'object_name': 'Supermarket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
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
        },
        u'octopus_user.usergeneratedbasket': {
            'Meta': {'object_name': 'UserGeneratedBasket'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'product_dict': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_user.OctopusUser']"}),
            'user_recommended_basket': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['octopus_user.UserRecommendedBasket']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'octopus_user.userinvited': {
            'Meta': {'object_name': 'UserInvited'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'primary_key': 'True'}),
            'is_invited': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'octopus_user.userproductslack': {
            'Meta': {'object_name': 'UserProductSlack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_groceries.Product']"}),
            'purchase_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'slack': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_user.OctopusUser']"})
        },
        u'octopus_user.userrecommendedbasket': {
            'Meta': {'object_name': 'UserRecommendedBasket'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_dict': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_user.OctopusUser']"})
        },
        u'octopus_user.usersettings': {
            'Meta': {'object_name': 'UserSettings'},
            'banned_abstract_products': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[]', 'max_length': '5000'}),
            'banned_meats': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[]', 'max_length': '5000'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'default_supermarket': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['octopus_groceries.Supermarket']", 'null': 'True', 'blank': 'True'}),
            'diet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_groceries.Diet']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_email_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'next_recommendation_email_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pre_user_creation_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'price_sensitivity': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'recommendation_email_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[]', 'max_length': '5000'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['octopus_user.OctopusUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['octopus_user']
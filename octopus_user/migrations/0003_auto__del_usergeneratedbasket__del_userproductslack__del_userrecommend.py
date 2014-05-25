# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserGeneratedBasket'
        db.delete_table(u'octopus_user_usergeneratedbasket')

        # Deleting model 'UserProductSlack'
        db.delete_table(u'octopus_user_userproductslack')

        # Deleting model 'UserRecommendedBasket'
        db.delete_table(u'octopus_user_userrecommendedbasket')

        # Adding model 'UserRelationship'
        db.create_table(u'octopus_user_userrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_followed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_followed', to=orm['octopus_user.OctopusUser'])),
            ('user_following', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_following', to=orm['octopus_user.OctopusUser'])),
        ))
        db.send_create_signal(u'octopus_user', ['UserRelationship'])

        # Deleting field 'UserSettings.pre_user_creation_hash'
        db.delete_column(u'octopus_user_usersettings', 'pre_user_creation_hash')

        # Deleting field 'UserSettings.people'
        db.delete_column(u'octopus_user_usersettings', 'people')

        # Deleting field 'UserSettings.tags'
        db.delete_column(u'octopus_user_usersettings', 'tags')

        # Deleting field 'UserSettings.days'
        db.delete_column(u'octopus_user_usersettings', 'days')

        # Deleting field 'UserSettings.diet'
        db.delete_column(u'octopus_user_usersettings', 'diet_id')

        # Deleting field 'UserSettings.banned_abstract_products'
        db.delete_column(u'octopus_user_usersettings', 'banned_abstract_products')

        # Deleting field 'UserSettings.price_sensitivity'
        db.delete_column(u'octopus_user_usersettings', 'price_sensitivity')

        # Deleting field 'UserSettings.banned_meats'
        db.delete_column(u'octopus_user_usersettings', 'banned_meats')

        # Adding field 'UserSettings.is_private'
        db.add_column(u'octopus_user_usersettings', 'is_private',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserSettings.zip_code'
        db.add_column(u'octopus_user_usersettings', 'zip_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserSettings.current_country'
        db.add_column(u'octopus_user_usersettings', 'current_country',
                      self.gf('django_countries.fields.CountryField')(default='GB', max_length=2),
                      keep_default=False)


        # Changing field 'UserSettings.default_supermarket'
        db.alter_column(u'octopus_user_usersettings', 'default_supermarket_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_groceries.Supermarket']))

    def backwards(self, orm):
        # Adding model 'UserGeneratedBasket'
        db.create_table(u'octopus_user_usergeneratedbasket', (
            ('user_recommended_basket', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['octopus_user.UserRecommendedBasket'], unique=True, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 28, 0, 0), auto_now_add=True, blank=True)),
            ('product_dict', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_user.OctopusUser'])),
        ))
        db.send_create_signal(u'octopus_user', ['UserGeneratedBasket'])

        # Adding model 'UserProductSlack'
        db.create_table(u'octopus_user_userproductslack', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_groceries.Product'])),
            ('slack', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('purchase_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 28, 0, 0), auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_user.OctopusUser'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'octopus_user', ['UserProductSlack'])

        # Adding model 'UserRecommendedBasket'
        db.create_table(u'octopus_user_userrecommendedbasket', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 28, 0, 0), auto_now_add=True, blank=True)),
            ('product_dict', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_user.OctopusUser'])),
        ))
        db.send_create_signal(u'octopus_user', ['UserRecommendedBasket'])

        # Deleting model 'UserRelationship'
        db.delete_table(u'octopus_user_userrelationship')

        # Adding field 'UserSettings.pre_user_creation_hash'
        db.add_column(u'octopus_user_usersettings', 'pre_user_creation_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=150, null=True, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'UserSettings.people'
        db.add_column(u'octopus_user_usersettings', 'people',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserSettings.tags'
        db.add_column(u'octopus_user_usersettings', 'tags',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[], max_length=5000),
                      keep_default=False)

        # Adding field 'UserSettings.days'
        db.add_column(u'octopus_user_usersettings', 'days',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserSettings.diet'
        db.add_column(u'octopus_user_usersettings', 'diet',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_groceries.Diet'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserSettings.banned_abstract_products'
        db.add_column(u'octopus_user_usersettings', 'banned_abstract_products',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[], max_length=5000),
                      keep_default=False)

        # Adding field 'UserSettings.price_sensitivity'
        db.add_column(u'octopus_user_usersettings', 'price_sensitivity',
                      self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=10, decimal_places=4),
                      keep_default=False)

        # Adding field 'UserSettings.banned_meats'
        db.add_column(u'octopus_user_usersettings', 'banned_meats',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[], max_length=5000),
                      keep_default=False)

        # Deleting field 'UserSettings.is_private'
        db.delete_column(u'octopus_user_usersettings', 'is_private')

        # Deleting field 'UserSettings.zip_code'
        db.delete_column(u'octopus_user_usersettings', 'zip_code')

        # Deleting field 'UserSettings.current_country'
        db.delete_column(u'octopus_user_usersettings', 'current_country')


        # Changing field 'UserSettings.default_supermarket'
        db.alter_column(u'octopus_user_usersettings', 'default_supermarket_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['octopus_groceries.Supermarket'], null=True))

    models = {
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
        u'octopus_user.userinvited': {
            'Meta': {'object_name': 'UserInvited'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 23, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'primary_key': 'True'}),
            'is_invited': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'octopus_user.userrelationship': {
            'Meta': {'object_name': 'UserRelationship'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_followed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_followed'", 'to': u"orm['octopus_user.OctopusUser']"}),
            'user_following': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_following'", 'to': u"orm['octopus_user.OctopusUser']"})
        },
        u'octopus_user.usersettings': {
            'Meta': {'object_name': 'UserSettings'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 23, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'current_country': ('django_countries.fields.CountryField', [], {'default': "'GB'", 'max_length': '2'}),
            'default_supermarket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['octopus_groceries.Supermarket']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'news_email_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'next_recommendation_email_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recommendation_email_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['octopus_user.OctopusUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['octopus_user']
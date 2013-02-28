# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EventUser.first_name'
        db.add_column(u'EventApp_eventuser', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='Facebook', max_length=200),
                      keep_default=False)

        # Adding field 'EventUser.last_name'
        db.add_column(u'EventApp_eventuser', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='User', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EventUser.first_name'
        db.delete_column(u'EventApp_eventuser', 'first_name')

        # Deleting field 'EventUser.last_name'
        db.delete_column(u'EventApp_eventuser', 'last_name')


    models = {
        u'EventApp.event': {
            'Meta': {'object_name': 'Event'},
            'age_days': ('django.db.models.fields.IntegerField', [], {}),
            'age_months': ('django.db.models.fields.IntegerField', [], {}),
            'age_years': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'EventApp.eventuser': {
            'Meta': {'object_name': 'EventUser'},
            'date_first_seen': ('django.db.models.fields.DateField', [], {}),
            'date_last_seen': ('django.db.models.fields.DateField', [], {}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'num_requests': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['EventApp']
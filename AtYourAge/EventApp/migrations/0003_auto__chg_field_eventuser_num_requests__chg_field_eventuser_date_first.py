# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'EventUser.num_requests'
        db.alter_column(u'EventApp_eventuser', 'num_requests', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'EventUser.date_first_seen'
        db.alter_column(u'EventApp_eventuser', 'date_first_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'EventUser.date_last_seen'
        db.alter_column(u'EventApp_eventuser', 'date_last_seen', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'EventUser.num_requests'
        raise RuntimeError("Cannot reverse this migration. 'EventUser.num_requests' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EventUser.date_first_seen'
        raise RuntimeError("Cannot reverse this migration. 'EventUser.date_first_seen' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EventUser.date_last_seen'
        raise RuntimeError("Cannot reverse this migration. 'EventUser.date_last_seen' and its values cannot be restored.")

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
            'date_first_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_last_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'num_requests': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['EventApp']
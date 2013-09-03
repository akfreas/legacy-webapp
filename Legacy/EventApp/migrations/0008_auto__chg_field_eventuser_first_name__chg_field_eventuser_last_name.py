# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'EventUser.first_name'
        db.alter_column(u'EventApp_eventuser', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'EventUser.last_name'
        db.alter_column(u'EventApp_eventuser', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'EventUser.first_name'
        raise RuntimeError("Cannot reverse this migration. 'EventUser.first_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EventUser.last_name'
        raise RuntimeError("Cannot reverse this migration. 'EventUser.last_name' and its values cannot be restored.")

    models = {
        u'EventApp.event': {
            'Meta': {'object_name': 'Event'},
            'age_days': ('django.db.models.fields.IntegerField', [], {}),
            'age_months': ('django.db.models.fields.IntegerField', [], {}),
            'age_years': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'figure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['EventApp.Figure']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'EventApp.eventuser': {
            'Meta': {'object_name': 'EventUser'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_first_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_last_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_requests': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'EventApp.figure': {
            'Meta': {'object_name': 'Figure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['EventApp']
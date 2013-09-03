# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field added_by on 'EventUser'
        db.create_table(u'EventApp_eventuser_added_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_eventuser', models.ForeignKey(orm[u'EventApp.eventuser'], null=False)),
            ('to_eventuser', models.ForeignKey(orm[u'EventApp.eventuser'], null=False))
        ))
        db.create_unique(u'EventApp_eventuser_added_by', ['from_eventuser_id', 'to_eventuser_id'])


    def backwards(self, orm):
        # Removing M2M table for field added_by on 'EventUser'
        db.delete_table('EventApp_eventuser_added_by')


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
            'added_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['EventApp.EventUser']", 'symmetrical': 'False'}),
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
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ApprovedBetaTesters.message'
        db.add_column(u'EventApp_approvedbetatesters', 'message',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ApprovedBetaTesters.message'
        db.delete_column(u'EventApp_approvedbetatesters', 'message')


    models = {
        u'EventApp.approvedbetatesters': {
            'Meta': {'object_name': 'ApprovedBetaTesters'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_used': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'EventApp.device': {
            'Meta': {'object_name': 'Device'},
            'associated_with': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['EventApp.EventUser']", 'symmetrical': 'False'}),
            'date_added': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_seen': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'device_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
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
            'date_added': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_first_seen': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_seen': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_requests': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'EventApp.figure': {
            'Meta': {'object_name': 'Figure'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_death': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['EventApp']
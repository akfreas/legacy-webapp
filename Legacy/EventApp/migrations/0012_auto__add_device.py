# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'EventApp_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_added', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_last_seen', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'EventApp', ['Device'])

        # Adding M2M table for field associated_with on 'Device'
        db.create_table(u'EventApp_device_associated_with', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('device', models.ForeignKey(orm[u'EventApp.device'], null=False)),
            ('eventuser', models.ForeignKey(orm[u'EventApp.eventuser'], null=False))
        ))
        db.create_unique(u'EventApp_device_associated_with', ['device_id', 'eventuser_id'])


    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table(u'EventApp_device')

        # Removing M2M table for field associated_with on 'Device'
        db.delete_table('EventApp_device_associated_with')


    models = {
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
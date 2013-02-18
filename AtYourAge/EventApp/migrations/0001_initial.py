# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'EventApp_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('male', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('age_years', self.gf('django.db.models.fields.IntegerField')()),
            ('age_months', self.gf('django.db.models.fields.IntegerField')()),
            ('age_days', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'EventApp', ['Event'])

        from django.core.management import call_command
        call_command("loaddata", "fixtures/initial_data.json")

        # Adding model 'EventUser'
        db.create_table(u'EventApp_eventuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_first_seen', self.gf('django.db.models.fields.DateField')()),
            ('date_last_seen', self.gf('django.db.models.fields.DateField')()),
            ('num_requests', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'EventApp', ['EventUser'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'EventApp_event')

        # Deleting model 'EventUser'
        db.delete_table(u'EventApp_eventuser')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_requests': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['EventApp']

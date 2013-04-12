# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Figure'
        db.create_table(u'EventApp_figure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'EventApp', ['Figure'])


        # Adding field 'Event.figure'
        db.add_column(u'EventApp_event', 'figure',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['EventApp.Figure'], null=True),
                      keep_default=False)


        events = orm.Event.objects.all()
        names = events.values("name").distinct()

        for name_dict in names:

            name = name_dict['name']

            try:
                figure = orm.Figure.get(name=name)
            except:
                figure = orm.Figure(name=name)
                figure.save()

            events_with_name = orm.Event.objects.filter(name=name)

            for event in events_with_name:
                event.figure = figure

                if event.image_url != None and figure.image_url == None:
                    figure.image_url = event.image_url
                    figure.save()

                event.save()


    def backwards(self, orm):
        # Deleting model 'Figure'
        db.delete_table(u'EventApp_figure')

        # Deleting field 'Event.figure'
        db.delete_column(u'EventApp_event', 'figure_id')


    models = {
        u'EventApp.event': {
            'Meta': {'object_name': 'Event'},
            'age_days': ('django.db.models.fields.IntegerField', [], {}),
            'age_months': ('django.db.models.fields.IntegerField', [], {}),
            'age_years': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'figure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['EventApp.Figure']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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
        },
        u'EventApp.figure': {
            'Meta': {'object_name': 'Figure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['EventApp']

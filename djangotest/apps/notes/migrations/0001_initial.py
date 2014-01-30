# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Notes'
        db.create_table(u'notes_notes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('text', self.gf('notes.models.UpperCaseTextField')()),
        ))
        db.send_create_signal(u'notes', ['Notes'])


    def backwards(self, orm):
        # Deleting model 'Notes'
        db.delete_table(u'notes_notes')


    models = {
        u'notes.notes': {
            'Meta': {'ordering': "['title']", 'object_name': 'Notes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('notes.models.UpperCaseTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['notes']
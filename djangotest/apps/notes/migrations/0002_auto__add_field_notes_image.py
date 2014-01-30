# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Notes.image'
        db.add_column(u'notes_notes', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True))


    def backwards(self, orm):
        # Deleting field 'Notes.image'
        db.delete_column(u'notes_notes', 'image')


    models = {
        u'notes.notes': {
            'Meta': {'ordering': "['title']", 'object_name': 'Notes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('notes.models.UpperCaseTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['notes']
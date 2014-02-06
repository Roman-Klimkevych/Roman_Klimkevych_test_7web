# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'notes_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'notes', ['Book'])

        # Adding M2M table for field books on 'Notes'
        m2m_table_name = db.shorten_name(u'notes_notes_books')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notes', models.ForeignKey(orm[u'notes.notes'], null=False)),
            ('book', models.ForeignKey(orm[u'notes.book'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notes_id', 'book_id'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'notes_book')

        # Removing M2M table for field books on 'Notes'
        db.delete_table(db.shorten_name(u'notes_notes_books'))


    models = {
        u'notes.book': {
            'Meta': {'object_name': 'Book'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'notes.notes': {
            'Meta': {'ordering': "['title']", 'object_name': 'Notes'},
            'books': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'notes'", 'symmetrical': 'False', 'to': u"orm['notes.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('notes.models.UpperCaseTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['notes']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Version'
        db.create_table(u'database_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Mod'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('status', self.gf('django.db.models.fields.CharField')(default='release', max_length=10, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('changelog', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('database', ['Version'])


    def backwards(self, orm):
        # Deleting model 'Version'
        db.delete_table(u'database_version')


    models = {
        'database.mod': {
            'Meta': {'ordering': "['name']", 'object_name': 'Mod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'database.version': {
            'Meta': {'ordering': "['date']", 'object_name': 'Version'},
            'changelog': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Mod']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'release'", 'max_length': '10', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['database']
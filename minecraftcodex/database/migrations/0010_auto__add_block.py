# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Block'
        db.create_table(u'database_block', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('main_texture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Texture'], null=True)),
            ('data_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'database', ['Block'])


    def backwards(self, orm):
        # Deleting model 'Block'
        db.delete_table(u'database_block')


    models = {
        u'database.block': {
            'Meta': {'object_name': 'Block'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'main_texture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Texture']", 'null': 'True'})
        },
        u'database.item': {
            'Meta': {'object_name': 'Item'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'main_texture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Texture']", 'null': 'True'})
        },
        'database.jarfile': {
            'Meta': {'object_name': 'JarFile'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'client'", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Version']"})
        },
        'database.mod': {
            'Meta': {'ordering': "['name']", 'object_name': 'Mod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'database.texture': {
            'Meta': {'object_name': 'Texture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'items'", 'max_length': '16'})
        },
        'database.version': {
            'Meta': {'ordering': "['date']", 'object_name': 'Version'},
            'changelog': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Mod']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'snapshot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'release'", 'max_length': '10', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.CharField', [], {'default': "'0.1.0'", 'max_length': '256'})
        }
    }

    complete_apps = ['database']
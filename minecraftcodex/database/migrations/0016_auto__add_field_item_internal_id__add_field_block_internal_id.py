# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.internal_id'
        db.add_column(u'database_item', 'internal_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Block.internal_id'
        db.add_column(u'database_block', 'internal_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.internal_id'
        db.delete_column(u'database_item', 'internal_id')

        # Deleting field 'Block.internal_id'
        db.delete_column(u'database_block', 'internal_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'database.block': {
            'Meta': {'object_name': 'Block'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'main_texture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Texture']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Version']", 'null': 'True', 'blank': 'True'})
        },
        u'database.item': {
            'Meta': {'object_name': 'Item'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'main_texture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Texture']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Version']", 'null': 'True', 'blank': 'True'})
        },
        'database.jarfile': {
            'Meta': {'object_name': 'JarFile'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'client'", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Version']"})
        },
        u'database.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'database.languagestring': {
            'Meta': {'object_name': 'LanguageString'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Language']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'database.mod': {
            'Meta': {'ordering': "['name']", 'object_name': 'Mod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'database.modelattribute': {
            'Meta': {'object_name': 'ModelAttribute'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {})
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
            'upcoming': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.CharField', [], {'default': "'0.1.0'", 'max_length': '256'})
        }
    }

    complete_apps = ['database']
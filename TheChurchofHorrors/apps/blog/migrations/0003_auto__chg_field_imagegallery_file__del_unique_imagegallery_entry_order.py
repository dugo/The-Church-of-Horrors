# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'ImageGallery', fields ['entry', 'order']
        db.delete_unique('blog_imagegallery', ['entry_id', 'order'])

        # Changing field 'ImageGallery.file'
        db.alter_column('blog_imagegallery', 'file', self.gf('filebrowser.fields.FileBrowseField')())

        # Changing field 'Entry.content'
        db.alter_column('blog_entry', 'content', self.gf('tinymce.models.HTMLField')())


    def backwards(self, orm):
        
        # Changing field 'ImageGallery.file'
        db.alter_column('blog_imagegallery', 'file', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Adding unique constraint on 'ImageGallery', fields ['entry', 'order']
        db.create_unique('blog_imagegallery', ['entry_id', 'order'])

        # Changing field 'Entry.content'
        db.alter_column('blog_entry', 'content', self.gf('django.db.models.fields.TextField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'blog.comment': {
            'Meta': {'ordering': "('time',)", 'object_name': 'Comment'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'blank': 'True', 'to': "orm['blog.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'blog.entry': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Entry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'to': "orm['auth.User']"}),
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '450', 'blank': 'True'}),
            'content': ('tinymce.models.HTMLField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'gallery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Section']"}),
            'show_gallery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Subsection']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'blog.imagegallery': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ImageGallery'},
            'adjust': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['blog.Entry']"}),
            'file': ('filebrowser.fields.FileBrowseField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'blog.section': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        'blog.subsection': {
            'Meta': {'ordering': "('sort',)", 'object_name': 'Subsection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'blog.subsectiontag': {
            'Meta': {'ordering': "('sort',)", 'unique_together': "(('subsection', 'tag'), ('sort', 'subsection'))", 'object_name': 'SubsectionTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['blog.Subsection']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taggit.Tag']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['blog']

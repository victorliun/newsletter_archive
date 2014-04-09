# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'NewsletterArchive.clouninary_image_id'
        db.alter_column(u'archive_newsletterarchive', 'clouninary_image_id', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'NewsletterArchiveWIP.clouninary_image_id'
        db.alter_column(u'archive_newsletterarchivewip', 'clouninary_image_id', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'NewsletterArchive.clouninary_image_id'
        db.alter_column(u'archive_newsletterarchive', 'clouninary_image_id', self.gf('django.db.models.fields.IntegerField')(default=1))

        # Changing field 'NewsletterArchiveWIP.clouninary_image_id'
        db.alter_column(u'archive_newsletterarchivewip', 'clouninary_image_id', self.gf('django.db.models.fields.IntegerField')(default=1))

    models = {
        u'archive.companydetail': {
            'Meta': {'object_name': 'CompanyDetail'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_added_by'", 'to': u"orm['auth.User']"}),
            'company_county': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'company_tags': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'domain_names': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subdomain_names': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'subscribe_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'unsubscribe_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'unsubscribe_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'archive.companystatstistics': {
            'Meta': {'object_name': 'CompanyStatstistics'},
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'companystatstistics'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['archive.CompanyDetail']"}),
            'last_update': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'newsletter_archived': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'newsletter_views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'archive.newsletterarchive': {
            'Meta': {'object_name': 'NewsletterArchive'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_by'", 'to': u"orm['auth.User']"}),
            'cloudinary_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'clouninary_image_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company'", 'to': u"orm['archive.CompanyDetail']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'6'", 'max_length': "'1'"})
        },
        u'archive.newsletterarchivewip': {
            'Meta': {'object_name': 'NewsletterArchiveWIP'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wip_added_by'", 'to': u"orm['auth.User']"}),
            'cloudinary_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'clouninary_image_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wip_company'", 'null': 'True', 'to': u"orm['archive.CompanyDetail']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path_from_phantomjs': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'newsletter_tags': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': "'1'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'archive.newslettertag': {
            'Meta': {'object_name': 'NewsletterTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.NewsletterArchiveWIP']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['archive']
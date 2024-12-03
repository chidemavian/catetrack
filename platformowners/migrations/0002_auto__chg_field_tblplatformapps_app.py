# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'tblplatformapps.app'
        db.alter_column(u'platformowners_tblplatformapps', 'app', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'tblplatformapps.app'
        db.alter_column(u'platformowners_tblplatformapps', 'app', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'platformowners.tblplatformapps': {
            'Meta': {'object_name': 'tblplatformapps'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'app_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformowners.tblplatformassessment': {
            'Meta': {'object_name': 'tblplatformassessment'},
            'assessment': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'assessment_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'assessment_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"})
        },
        u'platformowners.tblplatformclient': {
            'Meta': {'object_name': 'tblplatformclient'},
            'client_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'client_type_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformowners.tblplatformlga': {
            'Meta': {'object_name': 'tblplatformlga'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'platformowners.tblplatformowners': {
            'Meta': {'object_name': 'tblplatformowners'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'platformowners_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'platformowners.tblplatformsections': {
            'Meta': {'object_name': 'tblplatformsections'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'section_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'section_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformclient']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformowners.tblplatformstreams': {
            'Meta': {'object_name': 'tblplatformstreams'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stream': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stream_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsubsections']"})
        },
        u'platformowners.tblplatformsubjectdept': {
            'Meta': {'object_name': 'tblplatformsubjectdept'},
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dept_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsubsections']"})
        },
        u'platformowners.tblplatformsubjects': {
            'Meta': {'object_name': 'tblplatformsubjects'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'platformowners.tblplatformsubsections': {
            'Meta': {'object_name': 'tblplatformsubsections'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subsection': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subsection_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'platformowners.tblplatformterms': {
            'Meta': {'object_name': 'tblplatformterms'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['platformowners']
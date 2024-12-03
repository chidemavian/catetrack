# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'tblplatformowners'
        db.create_table(u'platformowners_tblplatformowners', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('platformowners_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('othername', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformowners'])

        # Adding model 'tblplatformlga'
        db.create_table(u'platformowners_tblplatformlga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('lga', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformlga'])

        # Adding model 'tblplatformclient'
        db.create_table(u'platformowners_tblplatformclient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('client_type_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformclient'])

        # Adding model 'tblplatformsections'
        db.create_table(u'platformowners_tblplatformsections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('section_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformclient'])),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('section_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformsections'])

        # Adding model 'tblplatformsubsections'
        db.create_table(u'platformowners_tblplatformsubsections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsections'])),
            ('subsection', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('subsection_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformsubsections'])

        # Adding model 'tblplatformapps'
        db.create_table(u'platformowners_tblplatformapps', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('app_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformapps'])

        # Adding model 'tblplatformterms'
        db.create_table(u'platformowners_tblplatformterms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('term_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformterms'])

        # Adding model 'tblplatformsubjects'
        db.create_table(u'platformowners_tblplatformsubjects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('subject_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformsubjects'])

        # Adding model 'tblplatformstreams'
        db.create_table(u'platformowners_tblplatformstreams', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsections'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsubsections'])),
            ('stream', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('stream_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformstreams'])

        # Adding model 'tblplatformsubjectdept'
        db.create_table(u'platformowners_tblplatformsubjectdept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dept', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsections'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsubsections'])),
            ('dept_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformsubjectdept'])

        # Adding model 'tblplatformassessment'
        db.create_table(u'platformowners_tblplatformassessment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformowners'])),
            ('assessment', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('assessment_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('assessment_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'platformowners', ['tblplatformassessment'])


    def backwards(self, orm):
        # Deleting model 'tblplatformowners'
        db.delete_table(u'platformowners_tblplatformowners')

        # Deleting model 'tblplatformlga'
        db.delete_table(u'platformowners_tblplatformlga')

        # Deleting model 'tblplatformclient'
        db.delete_table(u'platformowners_tblplatformclient')

        # Deleting model 'tblplatformsections'
        db.delete_table(u'platformowners_tblplatformsections')

        # Deleting model 'tblplatformsubsections'
        db.delete_table(u'platformowners_tblplatformsubsections')

        # Deleting model 'tblplatformapps'
        db.delete_table(u'platformowners_tblplatformapps')

        # Deleting model 'tblplatformterms'
        db.delete_table(u'platformowners_tblplatformterms')

        # Deleting model 'tblplatformsubjects'
        db.delete_table(u'platformowners_tblplatformsubjects')

        # Deleting model 'tblplatformstreams'
        db.delete_table(u'platformowners_tblplatformstreams')

        # Deleting model 'tblplatformsubjectdept'
        db.delete_table(u'platformowners_tblplatformsubjectdept')

        # Deleting model 'tblplatformassessment'
        db.delete_table(u'platformowners_tblplatformassessment')


    models = {
        u'platformowners.tblplatformapps': {
            'Meta': {'object_name': 'tblplatformapps'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
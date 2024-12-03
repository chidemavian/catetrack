# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'tblschool'
        db.create_table(u'business_tblschool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformadmin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('business_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformclient'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('web', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ig', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('fb', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('youtube', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school_code', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('logo_coloured', self.gf('django.db.models.fields.files.ImageField')(default='company_logo/thrift.png', max_length=100, null=True, blank=True)),
            ('logo_black', self.gf('django.db.models.fields.files.ImageField')(default='company_logo/thrift.png', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'business', ['tblschool'])

        # Adding model 'tblbranch'
        db.create_table(u'business_tblbranch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblschool'])),
            ('branch_code', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=300)),
        ))
        db.send_create_signal(u'business', ['tblbranch'])

        # Adding model 'tblbusinesssections'
        db.create_table(u'business_tblbusinesssections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsections'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinesssections'])

        # Adding model 'tblbusinesssubsections'
        db.create_table(u'business_tblbusinesssubsections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsubsections'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinesssubsections'])

        # Adding model 'tblbusinessapp'
        db.create_table(u'business_tblbusinessapp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('systemadmin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformapps'])),
        ))
        db.send_create_signal(u'business', ['tblbusinessapp'])

        # Adding model 'tblbusinessterms'
        db.create_table(u'business_tblbusinessterms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblschool'])),
            ('systemadmin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformterms'])),
            ('term_alias', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'business', ['tblbusinessterms'])

        # Adding model 'tblbusinessstream'
        db.create_table(u'business_tblbusinessstream', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssubsections'])),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformstreams'])),
            ('stream_alias', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinessstream'])

        # Adding model 'tblbusinesssubjectdept'
        db.create_table(u'business_tblbusinesssubjectdept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformowners.tblplatformsubjectdept'])),
            ('systemadmin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssubsections'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinesssubjectdept'])

        # Adding model 'tblbusinessaffective'
        db.create_table(u'business_tblbusinessaffective', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('affective', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('affective_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinessaffective'])

        # Adding model 'tblbusinesspsychomotive'
        db.create_table(u'business_tblbusinesspsychomotive', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platformowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('psychomotive', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('affective_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblbusinesspsychomotive'])

        # Adding model 'tblbusinessassessment'
        db.create_table(u'business_tblbusinessassessment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbranch'])),
            ('assessment', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblbusinesssections'])),
            ('max_in', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('assessment_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reportsheet', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'business', ['tblbusinessassessment'])

        # Adding model 'tblsystemsubjects'
        db.create_table(u'business_tblsystemsubjects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('section_code', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'business', ['tblsystemsubjects'])

        # Adding model 'tblaccountDetails'
        db.create_table(u'business_tblaccountdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblschool'])),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'business', ['tblaccountDetails'])

        # Adding model 'tblvas'
        db.create_table(u'business_tblvas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblschool'])),
            ('systemadmin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['platformadministrators.tblplatformadministrators'])),
            ('ux', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('otp', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'business', ['tblvas'])


    def backwards(self, orm):
        # Deleting model 'tblschool'
        db.delete_table(u'business_tblschool')

        # Deleting model 'tblbranch'
        db.delete_table(u'business_tblbranch')

        # Deleting model 'tblbusinesssections'
        db.delete_table(u'business_tblbusinesssections')

        # Deleting model 'tblbusinesssubsections'
        db.delete_table(u'business_tblbusinesssubsections')

        # Deleting model 'tblbusinessapp'
        db.delete_table(u'business_tblbusinessapp')

        # Deleting model 'tblbusinessterms'
        db.delete_table(u'business_tblbusinessterms')

        # Deleting model 'tblbusinessstream'
        db.delete_table(u'business_tblbusinessstream')

        # Deleting model 'tblbusinesssubjectdept'
        db.delete_table(u'business_tblbusinesssubjectdept')

        # Deleting model 'tblbusinessaffective'
        db.delete_table(u'business_tblbusinessaffective')

        # Deleting model 'tblbusinesspsychomotive'
        db.delete_table(u'business_tblbusinesspsychomotive')

        # Deleting model 'tblbusinessassessment'
        db.delete_table(u'business_tblbusinessassessment')

        # Deleting model 'tblsystemsubjects'
        db.delete_table(u'business_tblsystemsubjects')

        # Deleting model 'tblaccountDetails'
        db.delete_table(u'business_tblaccountdetails')

        # Deleting model 'tblvas'
        db.delete_table(u'business_tblvas')


    models = {
        u'business.tblaccountdetails': {
            'Meta': {'object_name': 'tblaccountDetails'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblschool']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'business.tblbranch': {
            'Meta': {'object_name': 'tblbranch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'branch_code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblschool']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '300'})
        },
        u'business.tblbusinessaffective': {
            'Meta': {'object_name': 'tblbusinessaffective'},
            'affective': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'affective_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'business.tblbusinessapp': {
            'Meta': {'object_name': 'tblbusinessapp'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformapps']"}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'systemadmin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"})
        },
        u'business.tblbusinessassessment': {
            'Meta': {'object_name': 'tblbusinessassessment'},
            'assessment': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'assessment_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_in': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'reportsheet': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"})
        },
        u'business.tblbusinesspsychomotive': {
            'Meta': {'object_name': 'tblbusinesspsychomotive'},
            'affective_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"}),
            'psychomotive': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'business.tblbusinesssections': {
            'Meta': {'object_name': 'tblbusinesssections'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'business.tblbusinessstream': {
            'Meta': {'object_name': 'tblbusinessstream'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformstreams']"}),
            'stream_alias': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssubsections']"})
        },
        u'business.tblbusinesssubjectdept': {
            'Meta': {'object_name': 'tblbusinesssubjectdept'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsubjectdept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssubsections']"}),
            'systemadmin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"})
        },
        u'business.tblbusinesssubsections': {
            'Meta': {'object_name': 'tblbusinesssubsections'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsubsections']"})
        },
        u'business.tblbusinessterms': {
            'Meta': {'object_name': 'tblbusinessterms'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblschool']"}),
            'systemadmin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformterms']"}),
            'term_alias': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'business.tblschool': {
            'Meta': {'object_name': 'tblschool'},
            'business_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformclient']"}),
            'fb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ig': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'logo_black': ('django.db.models.fields.files.ImageField', [], {'default': "'company_logo/thrift.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_coloured': ('django.db.models.fields.files.ImageField', [], {'default': "'company_logo/thrift.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'platformadmin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"}),
            'school_code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'youtube': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'business.tblsystemsubjects': {
            'Meta': {'object_name': 'tblsystemsubjects'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section_code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'business.tblvas': {
            'Meta': {'object_name': 'tblvas'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblschool']"}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'systemadmin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformadministrators.tblplatformadministrators']"}),
            'ux': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformadministrators.tblplatformadministrators': {
            'Meta': {'object_name': 'tblplatformadministrators'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformadministrators_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformowners.tblplatformapps': {
            'Meta': {'object_name': 'tblplatformapps'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'app_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformowners']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'platformowners.tblplatformclient': {
            'Meta': {'object_name': 'tblplatformclient'},
            'client_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'client_type_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['business']
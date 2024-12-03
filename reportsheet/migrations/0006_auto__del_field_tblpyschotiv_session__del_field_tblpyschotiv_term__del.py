# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'tblpyschotiv.session'
        db.delete_column(u'reportsheet_tblpyschotiv', 'session')

        # Deleting field 'tblpyschotiv.term'
        db.delete_column(u'reportsheet_tblpyschotiv', 'term')

        # Deleting field 'tblpyschotiv.klass'
        db.delete_column(u'reportsheet_tblpyschotiv', 'klass')

        # Deleting field 'tblpyschotiv.arm'
        db.delete_column(u'reportsheet_tblpyschotiv', 'arm')

        # Deleting field 'tblaffective.session'
        db.delete_column(u'reportsheet_tblaffective', 'session')

        # Deleting field 'tblaffective.term'
        db.delete_column(u'reportsheet_tblaffective', 'term')

        # Deleting field 'tblaffective.klass'
        db.delete_column(u'reportsheet_tblaffective', 'klass')

        # Deleting field 'tblaffective.arm'
        db.delete_column(u'reportsheet_tblaffective', 'arm')


    def backwards(self, orm):
        # Adding field 'tblpyschotiv.session'
        db.add_column(u'reportsheet_tblpyschotiv', 'session',
                      self.gf('django.db.models.fields.CharField')(default='ef', max_length=20),
                      keep_default=False)

        # Adding field 'tblpyschotiv.term'
        db.add_column(u'reportsheet_tblpyschotiv', 'term',
                      self.gf('django.db.models.fields.CharField')(default='ef', max_length=20),
                      keep_default=False)

        # Adding field 'tblpyschotiv.klass'
        db.add_column(u'reportsheet_tblpyschotiv', 'klass',
                      self.gf('django.db.models.fields.CharField')(default='ee', max_length=20),
                      keep_default=False)

        # Adding field 'tblpyschotiv.arm'
        db.add_column(u'reportsheet_tblpyschotiv', 'arm',
                      self.gf('django.db.models.fields.CharField')(default='eet', max_length=10),
                      keep_default=False)

        # Adding field 'tblaffective.session'
        db.add_column(u'reportsheet_tblaffective', 'session',
                      self.gf('django.db.models.fields.CharField')(default='fe', max_length=20),
                      keep_default=False)

        # Adding field 'tblaffective.term'
        db.add_column(u'reportsheet_tblaffective', 'term',
                      self.gf('django.db.models.fields.CharField')(default='rgrg', max_length=20),
                      keep_default=False)

        # Adding field 'tblaffective.klass'
        db.add_column(u'reportsheet_tblaffective', 'klass',
                      self.gf('django.db.models.fields.CharField')(default='ef', max_length=20),
                      keep_default=False)

        # Adding field 'tblaffective.arm'
        db.add_column(u'reportsheet_tblaffective', 'arm',
                      self.gf('django.db.models.fields.CharField')(default='efr', max_length=10),
                      keep_default=False)


    models = {
        u'business.tblbranch': {
            'Meta': {'object_name': 'tblbranch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'branch_code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblschool']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '300'})
        },
        u'business.tblbusinesssections': {
            'Meta': {'object_name': 'tblbusinesssections'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['platformowners.tblplatformsections']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        u'platformadministrators.tblplatformadministrators': {
            'Meta': {'object_name': 'tblplatformadministrators'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platformadministrators_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
        u'reportsheet.tblaffective': {
            'Meta': {'object_name': 'tblaffective'},
            'affective': ('django.db.models.fields.TextField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblclassroom']"})
        },
        u'reportsheet.tblannualsubjectrcords': {
            'Meta': {'object_name': 'tblannualsubjectrcords'},
            'annual_avg': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'classroo_subject_position_annual': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'grade_annual': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'remark_annual': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblclassroom']"}),
            'subject': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '125'}),
            'subject_avg_annual': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'subject_group': ('django.db.models.fields.CharField', [], {'default': "'ALL'", 'max_length': '125'}),
            'total_end_term_score': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '3'})
        },
        u'reportsheet.tblpyschotiv': {
            'Meta': {'object_name': 'tblpyschotiv'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'psychomotive': ('django.db.models.fields.TextField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblclassroom']"})
        },
        u'reportsheet.tblstudenttermlyrecord': {
            'Meta': {'object_name': 'tblstudenttermlyrecord'},
            'annual_rec': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reportsheet.tblannualsubjectrcords']"}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'class_ave_endterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'class_ave_midterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'class_teacher_comment_endterm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3000'}),
            'class_teacher_comment_midterm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3000'}),
            'classroom_position': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'days_absent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'days_open': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'days_present': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_term_start': ('django.db.models.fields.DateField', [], {'default': "'2000-01-01'", 'null': 'True', 'blank': 'True'}),
            'principal_comment_endterm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3000'}),
            'principal_comment_midterm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3000'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'stream_position': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'stu_ave_endterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'stu_ave_midterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblclassroom']"})
        },
        u'reportsheet.tblsubjectscores': {
            'Meta': {'object_name': 'tblsubjectScores'},
            'academic_rec': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reportsheet.tblstudenttermlyrecord']"}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'classroom_subject_avg_endterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'classroom_subject_avg_mid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'classroom_subposition_endterm': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'fifth_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'first_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'fourth_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'grade_endterm': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'remark_endterm': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'second_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbusinesssections']"}),
            'sixth_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'stream_subject_avg_endterm': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'stream_subposition_endterm': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '125'}),
            'subject_group': ('django.db.models.fields.CharField', [], {'default': "'ALL'", 'max_length': '125'}),
            'subject_teacher': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'subject_teacher_comment_endterm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3000'}),
            'third_ca': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'total_end_term_score': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '3'}),
            'total_mid_term_score': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '3'})
        },
        u'student.tblclassroom': {
            'Meta': {'object_name': 'tblclassroom'},
            'admissionno': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_arm': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_class': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_session': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'dayboarding': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblstudents']"}),
            'subclass': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'student.tblparents': {
            'Meta': {'object_name': 'tblparents'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'fatheraddress': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fathercode': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'fatheremail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fatherfirstname': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'fathernumber': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'fatheroccupation': ('django.db.models.fields.CharField', [], {'max_length': '175'}),
            'fatherothername': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'fatherpicture': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fathersurname': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motheraddress': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mothercode': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'motheremail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'motherfrstname': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'motherothername': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'motherphone': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'motherpicture': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mothersurname': ('django.db.models.fields.CharField', [], {'max_length': '275'})
        },
        u'student.tblstudents': {
            'Meta': {'object_name': 'tblstudents'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': "'2000-01-01'", 'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblparents']"}),
            'studentpicture': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['reportsheet']
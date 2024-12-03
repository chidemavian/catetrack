# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'tblclassroom.gone'
        db.delete_column(u'student_tblclassroom', 'gone')


    def backwards(self, orm):
        # Adding field 'tblclassroom.gone'
        db.add_column(u'student_tblclassroom', 'gone',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
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
        u'student.tblclassroom': {
            'Meta': {'object_name': 'tblclassroom'},
            'admissionno': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_arm': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_class': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_session': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'dayboarding': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
        },
        u'student.tblwithdrawnstudent': {
            'Meta': {'object_name': 'tblwithdrawnstudent'},
            'admitted_session': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblbranch']"}),
            'date_withdrawn': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.tblstudents']"}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['student']
from django.db import models

from student.models import *
from business.models import *
from setup.models import *





from django.db import models
from django.db.utils import DatabaseError
from django.db.models import Avg
from django.core.exceptions import FieldError


from student.models import *
from setup.models import *
from sysadmin.models import *
from academics.utils import *
from decimal import *




class tblannualsubjectrcords(models.Model): 
    branch=models.ForeignKey(tblbranch)
    student = models.ForeignKey(tblclassroom)
    section=models.ForeignKey(tblbusinesssections)

    subject = models.CharField('Subject', max_length=125, default=0)

    subject_group = models.CharField('Subject Group', max_length=125, default='ALL')
    num = models.IntegerField(editable=False)



    total_end_term_score = models.CharField('Term Score', max_length=3, default=0)
    total_end_term_score = models.CharField('Term Score', max_length=3, default=0)
    total_end_term_score = models.CharField('Term Score', max_length=3, default=0)


    annual_grade = models.CharField('Grade', max_length=3, default= 'F')

    annual_remark = models.CharField('Remark', max_length=60)   

    annual_subject_avg = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)


    annual_subject_position_classroom = models.CharField('Position', max_length=10, default='N/A')
    annual_subject_position_stream =models.CharField('Position', max_length=10, default='N/A')

    annual_avg = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)

    def __unicode__(self):
        return u'%s %s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' %(self.remarks, self.academic_rec.student.subclass, self.term,self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session,self.subject,self.first_ca,self.second_ca,self.sixth_ca,self.end_term_score,self.remark,self.annual_avg)




class tblstudenttermlyrecord(models.Model):
    annual_rec = models.ForeignKey(tblannualsubjectrcords)
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)	
    student = models.ForeignKey(tblclassroom)


    days_open = models.IntegerField('No. of Days School Opened', default=0)
    days_present = models.IntegerField('Days Present', default=0)
    days_absent = models.IntegerField('Days Absent', default=0)
    next_term_start = models.DateField('Next Term Begins', null=True,blank=True,default='2000-01-01')

    stream_position = models.CharField('Class Position', max_length=10, default='N/A')
    classroom_position = models.CharField('Class Room Position', max_length = 10, default = 'N/A')

    

    stu_ave_midterm = models.DecimalField('Student Average Mid term', decimal_places=2, max_digits=5, default=0)
    stu_ave_endterm = models.DecimalField('Student Average End term', decimal_places=2, max_digits=5, default=0)

    class_ave_midterm  = models.DecimalField('Class Average Mid term', decimal_places=2, max_digits=5, default=0)
    class_ave_endterm = models.DecimalField('Class Average End term', decimal_places=2, max_digits=5, default=0)



    class_teacher_comment_midterm  = models.CharField('Classteacher Mid term Comment',max_length=3000, default='')
    class_teacher_comment_endterm = models.CharField("Class Teacher's End term Comment", max_length=3000, default='')

    principal_comment_midterm = models.CharField('principal mid term Comment',  max_length =3000, default='')
    principal_comment_endterm = models.CharField("Principal's End term  Comment", max_length=3000, default='')



    def __unicode__(self):
		return  u'classave: %s,Name: %s, Admission No: %s , Class: %s, Arm: %s,Session: %s' %(self.classAve, self.student.fullname,self.student.admissionno,self.klass,self.arm,self.session)





score = (('A', 'A - Exceptionally Exhibited'), ('B', 'B - Appreciably Demonstrated'),
        ('C', 'C - Satisfactorily Displayed'), ('D', 'D - Needs Improvement'),
        ('N/A', 'Not Available'))




class tblsubjectScores(models.Model):
    academic_rec = models.ForeignKey(tblstudenttermlyrecord)

    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)  

    subject = models.CharField('Subject', max_length=125, default=0)

    subject_group = models.CharField('Subject Group', max_length=125, default='ALL')
    num = models.IntegerField()




    first_ca = models.CharField('First CA', max_length=2, default=0)
    second_ca = models.CharField('Second CA', max_length=2, default=0)
    third_ca = models.CharField('Third CA',max_length=2, default=0)
    fourth_ca = models.CharField('Fourth CA', max_length=2, default=0)
    fifth_ca = models.CharField('Fifth CA', max_length=2, default=0)
    sixth_ca = models.CharField('Sixth CA', max_length=2, default=0)


    total_mid_term_score = models.CharField('Midterm', max_length=3, default=0)
    total_end_term_score = models.CharField('Term Score', max_length=3, default=0)

    grade_endterm = models.CharField('Grade', max_length=3, default= 'F')

    remark_endterm = models.CharField('Remark', max_length=60)   

    stream_subject_avg_endterm = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)
    classroom_subject_avg_endterm = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)
    
    classroom_subject_avg_mid = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)

    stream_subposition_endterm = models.CharField('Position', max_length=10, default='N/A')
    classroom_subposition_endterm = models.CharField('Position', max_length=10, default='N/A')

    subject_teacher_comment_endterm = models.CharField("Class Teacher's End term Comment", max_length=3000, default='')


    subject_teacher = models.CharField('Subject Teacher', max_length=200,null=True, default=models.NOT_PROVIDED)

      


    def __unicode__(self):
        return u'%s %s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' %(self.remarks, self.academic_rec.student.subclass, self.term,self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session,self.subject,self.first_ca,self.second_ca,self.sixth_ca,self.end_term_score,self.remark,self.annual_avg)

    def save(self, **kwargs):
      self.mid_term_score = int(self.first_ca)  + int(self.second_ca) + int(self.third_ca)
      self.end_term_score = int(self.first_ca)  + int(self.second_ca) + int(self.third_ca) + int(self.fourth_ca)  + int(self.fifth_ca) + int(self.sixth_ca)







grading = (('A', 'A (80 - 100)'), ('B', 'B (65 - 79)'), ('C', 'C (55 - 64)'),
           ('P', 'P (45 - 54)'), ('F', 'F (0 - 4)'))




class tblaffective(models.Model): 
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    student = models.ForeignKey(tblclassroom)


    affective = models.TextField()

   


class tblpyschotiv(models.Model): 
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    student = models.ForeignKey(tblclassroom)


    psychomotive = models.TextField()

   

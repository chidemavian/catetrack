from django.db import models
from setup.models import *
#from utils import PhoneNumberValidator
# from PIL import Image

from business.models import *

# from platformowners.models import *









class tblmidtermhighest(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    highest_score = models.CharField(max_length=3)
    reportsheet = models.CharField(max_length=30)




class tblmidtermbreakdown(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    term_highest=models.ForeignKey(tblmidtermhighest)
    assessment = models.CharField(max_length=30)
    max_score= models.CharField(max_length=5)




    
class tblbusinessstreamrooms(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    subsection=models.ForeignKey(tblbusinesssubsections)
    stream=models.ForeignKey(tblbusinessstream)
    room = models.CharField(max_length=20)
    status= models.BooleanField()
    def __unicode__(self):
        return '%s %s %s'%(self.section,self.room,self.status)






class tblbusinesssubject(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    subsection=models.ForeignKey(tblbusinesssubsections)
    subject = models.CharField(max_length=75)
    subject_code=models.CharField(max_length=40)
    category=models.CharField(max_length=40)
    department=models.ForeignKey(tblbusinesssubjectdept)
    status= models.BooleanField()

    def __unicode__(self):
        return '%s %s %s'%(self.subject,self.subject_code,self.status)





class tblcognitivegrade(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    subsection=models.ForeignKey(tblbusinesssubsections)
    vrange = models.CharField(max_length=75)
    grade=models.CharField(max_length=40)
    remark=models.CharField(max_length=40)

    def __unicode__(self):
        return '%s %s %s'%(self.vrange,self.grade,self.remark)


class tblaffectivegrade(models.Model):
    branch=models.ForeignKey(tblbranch)
    section=models.ForeignKey(tblbusinesssections)
    subsection=models.ForeignKey(tblbusinesssubsections)
    vrange = models.CharField(max_length=75)
    remark=models.CharField(max_length=40)

    def __unicode__(self):
        return '%s %s'%(self.vrange,self.remark)

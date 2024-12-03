
from django.db import models

from business.models import *

from platformowners.models import *



class tblstaff(models.Model):
	branch=models.ForeignKey(tblbranch)
	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername=models.CharField(max_length=20)
	email=models.EmailField(max_length=200)
	phone=models.CharField(max_length=11)
	photo=models.ImageField(upload_to='staff-pix', null=True,blank=True,default='staff-pix/user.png')
	staff_code=models.CharField(max_length=41)
	status= models.BooleanField()
	
	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.othername)
		





class tblsectionmanager(models.Model):
	platformowner=models.ForeignKey(tblplatformowners)
	branch=models.ForeignKey(tblbranch)
	staff=models.ForeignKey(tblstaff)
	section=models.ForeignKey(tblbusinesssections)

	manager_code=models.CharField(max_length=40)
	status = models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.section,self.status)

from django.db import models

from platformowners.models import *






class tblplatformadministrators(models.Model):
	platformowner = models.ForeignKey(tblplatformowners)
	email = models.EmailField()
	platformadministrators_code = models.CharField(max_length=20)
	status= models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.status,self.platformowner)


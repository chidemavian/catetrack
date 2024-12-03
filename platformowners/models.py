from django.db import models


# from business.models import *


class tblplatformowners(models.Model):
	email = models.EmailField()
	platformowners_code = models.CharField(max_length=20)
	surname = models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername= models.CharField(max_length=20)
	status= models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.surname,self.firstname)






class tblplatformlga(models.Model):
	state = models.CharField('State', max_length=25)
	lga = models.CharField('L.G.A.', max_length=25)

	def __unicode__(self):
		return '%s %s'%(self.state,self.lga)


class tblplatformclient(models.Model):
	client_type=models.CharField(max_length=20)
	client_type_code = models.CharField(max_length=20)
	status= models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.client_type,self.client_type_code,self.status)


class tblplatformsections(models.Model):
	platformowner=models.ForeignKey(tblplatformowners)
	section_type= models.ForeignKey(tblplatformclient)
	section= models.CharField(max_length=20)
	section_code = models.CharField(max_length=20)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.platformowner,self.section,self.section_code)




class tblplatformsubsections(models.Model):
	section=models.ForeignKey(tblplatformsections)
	subsection= models.CharField(max_length=20)
	subsection_code = models.CharField(max_length=20)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.section,self.subsection,self.subsection_code)





class tblplatformapps(models.Model):
	app= models.CharField(max_length=200)
	app_code = models.CharField(max_length=20)
	platformowner=models.ForeignKey(tblplatformowners)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.app,self.app_code,self.status)



class tblplatformterms(models.Model):
	term= models.CharField(max_length=20)
	term_code = models.CharField(max_length=20)
	platformowner=models.ForeignKey(tblplatformowners)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.term,self.term_code,self.status)



class tblplatformsubjects(models.Model):
	subject= models.CharField(max_length=20)
	subject_code= models.CharField(max_length=20)
	status = models.CharField(max_length=20)
	section= models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.subject,self.section,self.section_code)




class tblplatformstreams(models.Model):
	platformowner=models.ForeignKey(tblplatformowners)
	section= models.ForeignKey(tblplatformsections)
	subsection= models.ForeignKey(tblplatformsubsections)
	stream = models.CharField(max_length=20)
	stream_code = models.CharField(max_length=20)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.stream,self.stream_code,self.status)




class tblplatformsubjectdept(models.Model):
	dept = models.CharField(max_length=20)
	platformowner=models.ForeignKey(tblplatformowners)
	section= models.ForeignKey(tblplatformsections)
	subsection= models.ForeignKey(tblplatformsubsections)
	dept_code = models.CharField(max_length=20)
	status= models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.dept,self.dept_code,self.status)



class tblplatformassessment(models.Model): #delete this tabl
	platformowner=models.ForeignKey(tblplatformowners)
	assessment = models.CharField(max_length=5)
	assessment_code = models.CharField(max_length=30)
	assessment_status = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.assessment,self.assessmnt_code,self.assessmnt_status)





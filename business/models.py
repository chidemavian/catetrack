from django.db import models

from platformadministrators.models import * 

# from staff.models import tblstaff

from staff.models import  *


class tblschool(models.Model): #school name
	platformadmin = models.ForeignKey(tblplatformadministrators)
	business_type = models.ForeignKey(tblplatformclient)
	name =models.CharField(max_length=500)
	web = models.CharField(max_length=200)
	ig=models.CharField(max_length=50)
	twitter = models.CharField(max_length=40)
	fb= models.CharField(max_length=50)
	youtube=models.CharField(max_length=50)
	school_code=models.CharField(max_length=15)
	status= models.BooleanField()
	logo_coloured = models.ImageField(upload_to='company_logo', null=True,
		blank=True,default='company_logo/thrift.png')
	

	logo_black = models.ImageField(upload_to='company_logo', null=True,
		blank=True,default='company_logo/thrift.png')

	def __unicode__(self):
		return '%s %s %s'%(self.name,self.web,self.status)




class tblbranch(models.Model): #branches
	address = models.CharField(max_length=300)
	company=models.ForeignKey(tblschool)
	branch_code=models.CharField(max_length=40)	
	phone= models.CharField(max_length=11)
	status = models.BooleanField(max_length=300)
	def __unicode__(self):
		return '%s %s %s'%(self.address,self.phone,self.status)



class tblbusinesssections(models.Model): #sections
	section=models.ForeignKey(tblplatformsections)
	branch=models.ForeignKey(tblbranch)
	status = models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.section.section,self.branch,self.status)




class tblbusinesssubsections(models.Model): #subsections
	branch=models.ForeignKey(tblbranch)
	section=models.ForeignKey(tblbusinesssections)
	subsection=models.ForeignKey(tblplatformsubsections)
	status = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.subsection,self.section)




class tblbusinessapp(models.Model): #servie
	branch=models.ForeignKey(tblbranch)
	systemadmin = models.ForeignKey(tblplatformadministrators)
	section=models.ForeignKey(tblbusinesssections)
	app = models.ForeignKey(tblplatformapps)

	def __unicode__(self):
		return '%s %s %s'%(self.app,self.systemadmin,self.branch)




class tblbusinessterms(models.Model): #term names
	school=models.ForeignKey(tblschool)
	systemadmin = models.ForeignKey(tblplatformadministrators)
	term = models.ForeignKey(tblplatformterms)
	term_alias= models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.term,self.systemadmin,self.branch)



class tblbusinessstream(models.Model): #stream names
	branch=models.ForeignKey(tblbranch)
	section=models.ForeignKey(tblbusinesssections)
	subsection=models.ForeignKey(tblbusinesssubsections)
	stream=models.ForeignKey(tblplatformstreams)
	stream_alias = models.CharField(max_length=20)
	status= models.BooleanField()
	def __unicode__(self):
		return '%s %s %s'%(self.section,self.stream_alias,self.status)






class tblbusinesssubjectdept(models.Model): #subject departments
	department = models.ForeignKey(tblplatformsubjectdept)
	systemadmin = models.ForeignKey(tblplatformadministrators)
	branch=models.ForeignKey(tblbranch)
	section=models.ForeignKey(tblbusinesssections)
	subsection=models.ForeignKey(tblbusinesssubsections)	
	status= models.BooleanField()
	def __unicode__(self):
		return '%s %s %s'%(self.department,self.branch,self.status)






class tblbusinessaffective(models.Model): #affective domains
	platformowner=models.ForeignKey(tblplatformadministrators)
	branch=models.ForeignKey(tblbranch)
	section=models.ForeignKey(tblbusinesssections)
	affective = models.CharField(max_length=50)
	affective_code = models.CharField(max_length=50)
	status = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.affective,self.status,self.affective_code)


class tblbusinesspsychomotive(models.Model): #psychomotive domains
	platformowner=models.ForeignKey(tblplatformadministrators)
	branch=models.ForeignKey(tblbranch)
	section=models.ForeignKey(tblbusinesssections)
	psychomotive = models.CharField(max_length=20)
	affective_code = models.CharField(max_length=20)
	status = models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.psychomotive,self.status,self.psychomotive_code)


 

class tblbusinessassessment(models.Model):
	branch=models.ForeignKey(tblbranch)
	assessment=models.CharField(max_length=50)
	section=models.ForeignKey(tblbusinesssections)
	max_in = models.CharField(max_length=20)
	assessment_status= models.BooleanField()
	reportsheet = models.CharField(max_length=20)
	def __unicode__(self):
		return '%s %s %s'%(self.assessment,self.max_in,self.assessment_status)



class tblsystemsubjects(models.Model):
	# section=models.ForeignKey(tblsections)
	subject=models.CharField(max_length=40)
	section_code=models.CharField(max_length=40)
	code= models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.section,self.subject,self.code)




class tblaccountDetails(models.Model):
	company=models.ForeignKey(tblschool) #use tblbranch instaed
	account=models.CharField(max_length=40)
	bank = models.CharField(max_length=10)
	code= models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.company,self.bank,self.code)


		



class tblvas(models.Model):
	company=models.ForeignKey(tblschool) #use tblbranch instaed
	systemadmin  = models.ForeignKey(tblplatformadministrators)
	ux= models.BooleanField()
	otp= models.BooleanField()
	sms= models.BooleanField()
	email= models.BooleanField()
	

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.otp,self.partner)

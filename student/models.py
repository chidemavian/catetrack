from django.db import models
from setup.models import *
from business.models import *







class tblparents(models.Model):
    branch=models.ForeignKey(tblbranch)
    fathersurname = models.CharField("Name", max_length=275)
    fatherfirstname = models.CharField("Name", max_length=275)
    fatherothername = models.CharField("Name", max_length=275)
    fatheraddress = models.CharField('Address', max_length=200)
    fathernumber = models.CharField('Phone Number', max_length=35, null=True,blank=True )#validators=[PhoneNumberValidator]s
    fatheroccupation = models.CharField('Occupation', max_length=175)
    fatheremail = models.CharField('Father E-mail', max_length=200,null=True,blank=True)
    fatherpicture = models.ImageField('Passport', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')
    fathercode = models.CharField("Name", max_length=275)
    
    
    mothersurname = models.CharField("Name", max_length=275)
    motherfrstname = models.CharField("Name", max_length=275)
    motherothername = models.CharField("Name", max_length=275)
    motheraddress = models.CharField('Address', max_length=200)
    motherphone = models.CharField('Phone Number', max_length=35, null=True,blank=True )#validators=[PhoneNumberValidator]s
    motheremail = models.CharField('Father E-mail', max_length=200,null=True,blank=True)
    motherpicture = models.ImageField('Passport', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')
    mothercode = models.CharField("Name", max_length=275)


    def __unicode__(self):
        return u'%s  %s %s' %(self.fathersurname,self.fatheremail,self.motherphone)



class tblstudents(models.Model):
    branch=models.ForeignKey(tblbranch)
    parent=models.ForeignKey(tblparents)
    firstname = models.CharField('First Name', max_length=75)
    surname = models.CharField('Surname', max_length=75)
    othername = models.CharField('Other Names', max_length=75, null=True, blank=True)
    address = models.CharField('Address', max_length=200)
    gender = models.CharField('Sex',max_length=10, choices=(('Male', 'Male'),('Female', 'Female')))
    
    birth_date = models.DateField('Date of Birth',null=True,blank=True,default='2000-01-01')
    birth_place = models.CharField('Place of Birth', max_length=75)
    # state_of_origin = models.CharField('State of Origin', max_length=75, choices=states)
    lga = models.CharField('L.G.A.', max_length=75)
    studentpicture = models.ImageField('Passport', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')
    gone = models.BooleanField('Gone', default=False, editable=True)

    def __unicode__(self):
        return '%s %s %s' %(self.firstname,self.surname,self.othername)
    


class tblclassroom(models.Model):
    branch=models.ForeignKey(tblbranch)
    student=models.ForeignKey(tblstudents)
    
    admitted_session = models.CharField('Session Admitted', max_length=25, null=True, blank=True)
    term = models.CharField('Term', max_length=20, null=True)


    admitted_class = models.CharField('Admitted Class', max_length=25)
    admitted_arm = models.CharField('Arm', max_length=25)

    admissionno = models.CharField('Admission Number', max_length=25)

    dayboarding = models.CharField('Day/Boarding', max_length=25, choices=(('Day', 'Day'), ('Boarding', 'Boarding')))
    gone = models.BooleanField('Gone', default=False, editable=True)

    subclass = models.CharField('Subject Category', max_length=25)

    def __unicode__(self):
        return '%s %s %s' %(self.admissionno,self.admitted_class,self.admitted_arm)




class tblwithdrawnstudent(models.Model):
    branch=models.ForeignKey(tblbranch)
    student=models.ForeignKey(tblstudents)

    reason = models.TextField('Reason for Withdrawal')
    date_withdrawn = models.DateField('Date of Withdrawal')
    admitted_session = models.CharField('Withdrwal Session',max_length=15)
    userid = models.CharField("User Id",max_length= 250)

    def __unicode__(self):
        return '%s %s %s' %(self.student,self.date_withdrawn,self.reason)



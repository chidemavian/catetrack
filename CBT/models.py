from django.db import models


from student.models import Student


from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver



state = terms_list = (('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'))

# Create your models here.





class cbtcurrentquestion(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    number = models.CharField('number',max_length=10)

    def __unicode__(self):
        return u'%s-%s-%s-%s' %(self.exam_type,self.subject,self.student,self.number)




class tblquestion(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    term = models.CharField('Term',max_length=10)
    topic = models.CharField('Topic',max_length=1000, null=False,blank=True)
    instruction_from = models.CharField('From', max_length=975)
    instruction_to = models.CharField('From', max_length=975)
    qstn = models.CharField('Question', max_length=975)
    image = models.ImageField('Image', upload_to='questions', null=True,blank=True,default='studentpix/user.png')
    section = models.CharField('Section', max_length=20,default=0)


    def __unicode__(self):
        return '%s %s %s'%(self.exam_type,self.subject,self.qstn)



class cbtold(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    question = models.ForeignKey(tblquestion,null=False,blank=False,choices=state,default='INACTIVE')
    klass = models.CharField('Class',max_length=10)
    qstcode = models.CharField('Question ID',default=0, max_length=10)

    def __unicode__(self):

        return  u'%s %s %s %s' % (self.qstcode,self.subject)



class tbloptions(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Options')
    a = models.CharField('Option A', max_length=7500)
    b = models.CharField('Option B', max_length=7500)
    c = models.CharField('Option C', max_length=7500)
    d = models.CharField('Option D', max_length=7500)
    e = models.CharField('Option E', max_length=7500)


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)    
  


class tbloptioni(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Optioni')
    a = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    b = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    c = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    d = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    e = models.ImageField('Image', upload_to='questions',default='questions/user.png')


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)

class tblans(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Transaction')
    ans = models.CharField('Answer', max_length=75)
    option = models.CharField('Option', max_length=7500,default=0)

    def __unicode__(self):
        return u' a : %s, b:  %s ' % (self.ans, self.option)


class cbttrans(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    question = models.ForeignKey(tblquestion,null=False,blank=False,choices=state,default='INACTIVE')
    stu_ans = models.CharField('Answer',max_length=10)
    score = models.IntegerField('Score', default=0)
    qstcode = models.CharField('Question ID',default=0,max_length=10)
    status = models.CharField('Status',default=0,max_length=10)
    no = models.CharField('Count',default=0,max_length=10)
    

    def __unicode__(self):
        return u'%s-%s-%s' %(self.exam_type,self.subject,self.score)




class tbltheory(models.Model):
	exam_type = models.CharField('Exam Type', max_length=375)
	subject = models.CharField('Subject', max_length=75)
	session = models.CharField('Session', max_length=75, null=True, blank=True)
	klass = models.CharField('Class', max_length=20)
	term = models.CharField('Term',max_length=10)
	image = models.ImageField('Image', upload_to='questions',default='questions/user.png')


	def __unicode__(self):
		return u' exam_type : %s ,subject : %s , term : %s' % (self.exam_type,self.subject,self.term)



class tblcbtexams(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    status = models.CharField('Status', max_length=75, null=False, blank=False)


    def __unicode__(self):
        return '%s %s'%(self.exam_type,self.status)

class tblcbtuser(models.Model):
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    subject = models.CharField('Subject',max_length=100)
    email = models.EmailField()

    def __unicode__(self):
    	return u' exam : %s ,subject : %s , term : %s' % (self.exam_type,self.subject,self.term)



class tblcbtsubject(models.Model):
    duration = models.CharField('Duration', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    term = models.CharField('Term',max_length=10)
    exam_type = models.CharField('Exam_type', max_length=75)
    st_date = models.DateField('Date',max_length=10)
    st_time = models.TimeField('Time', max_length=9)
    status = models.CharField('Status',null=True,blank=True,max_length=60,default='INACTIVE')

    def __unicode__(self):

    	return u'%s-%s' % (self.subject,self.term)



class scheduled(models.Model):
    session = models.CharField('Session', max_length=375)
    assessment = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
   
    def __unicode__(self):
        return u'%s-%s-%s' %(self.assessment,self.subject,self.term)




class donesubjects(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)


    def __unicode__(self):
        return u'%s-%s-%s' %(self.exam_type,self.subject,self.term)










class tblcbtcurrentquestioneng(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    number = models.CharField('number',max_length=10)
    # qtype = models.CharField('Source',max_length=10)

    def __unicode__(self):
        return u'%s-%s-%s-%s' %(self.exam_type,self.subject,self.student,self.number)



class tblcbtoldeng(models.Model):
    question = models.ForeignKey(tblcbtcurrentquestioneng,null=False,related_name='qst')

    qstno = models.CharField('Class',max_length=10)
    qstcode = models.CharField('Question ID',default=0, max_length=15)
    groupcode = models.CharField('Question ID',default=0,max_length=15)
    category= models.CharField('Category',default=0,max_length=15)
    


    def __unicode__(self):

        return  u'%s %s %s %s' % (self.qstcode,self.qstno,self.groupcode,self.category)




class tblcbttranscomp(models.Model):
    session = models.CharField('Session', max_length=375)
    term = models.CharField('Term',max_length=10)
    subject = models.CharField('Subject', max_length=20) 
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True) 
    stu_ans = models.CharField('Answer',max_length=100)
    score = models.IntegerField('Score', default=0)
    status = models.CharField('Status',default=0,max_length=10)
    qno = models.CharField('Count',default=0,max_length=10)

    qstcode = models.CharField('Question ID',default=0,max_length=15)
    category= models.CharField('Category',default=0,max_length=15)
    groupcode = models.CharField('Question ID',default=0,max_length=15)

    def __unicode__(self):
        return u'%s-%s-%s' %(self.exam_type,self.subject,self.score)





class tblcomprehension(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    term = models.CharField('Term',max_length=10)
    qstimage = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    p1 = models.CharField('p1', max_length=1975)
    p2 = models.CharField('p2', max_length=2975)
    p3 = models.CharField('p3', max_length=2975)
    p4 = models.CharField('p4', max_length=2975)
    p5 = models.CharField('p5', max_length=2975)

    def __unicode__(self):
        return '%s %s %s'%(self.exam_type,self.subject,self.term)





class tblcomprehensionqst(models.Model):
    comprehension = models.ForeignKey(tblcomprehension, related_name='Opt')

    code1 = models.CharField('code', max_length=2975)        
    qstcode = models.CharField('Question code', max_length=975)
    q1 = models.CharField('Section', max_length=2000,default=0)

    def __unicode__(self):
        return '%s %s %s'%(self.comprehension,self.code1,self.q1)



class tbloptionseng(models.Model):
    qstn = models.ForeignKey(tblcomprehensionqst, related_name='Options')
    a = models.CharField('Option A', max_length=7500)
    b = models.CharField('Option B', max_length=7500)
    c = models.CharField('Option C', max_length=7500)
    d = models.CharField('Option D', max_length=7500)
    e = models.CharField('Option E', max_length=7500)

    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)


class tblanscomp(models.Model):
    qstn = models.ForeignKey(tblcomprehensionqst, related_name='engqst')
    ans = models.CharField('Answer', max_length=75)
    option = models.CharField('Option', max_length=7500,default=0)

    def __unicode__(self):
        return u' a : %s, b:  %s ' % (self.ans, self.option)



class tblblock(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    term = models.CharField('Term',max_length=10)
    klass = models.CharField('Class',max_length=10)    
    instruction = models.CharField('Instruction', max_length=1975)
    code = models.CharField('Code', max_length=2975)
    def __unicode__(self):
        return '%s %s %s'%(self.exam_type,self.instruction,self.code)





class tblblockquestion(models.Model):
    block = models.ForeignKey(tblblock, related_name='block')
    q1 = models.CharField('Section', max_length=2000,default=0)
    qstcode = models.CharField('Code', max_length=2000,default=0)
    image = models.ImageField('Image', upload_to='questions', null=True,blank=True,default='studentpix/user.png')



    def __unicode__(self):
        return '%s %s'%(self.block,self.q1)


@receiver(post_delete, sender=tblblockquestion)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=tblblockquestion)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass



class tbloptionblk(models.Model):
    qstn = models.ForeignKey(tblblockquestion, related_name='blkOptions')
    a = models.CharField('Option A', max_length=7500)
    b = models.CharField('Option B', max_length=7500)
    c = models.CharField('Option C', max_length=7500)
    d = models.CharField('Option D', max_length=7500)
    e = models.CharField('Option E', max_length=7500)

    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)


class tbloptionblki(models.Model):
    qstn = models.ForeignKey(tblblockquestion, related_name='Optionimage')
    a = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    b = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    c = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    d = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    e = models.ImageField('Image', upload_to='questions',default='questions/user.png')


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)



@receiver(post_delete, sender=tbloptionblki)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.a.delete(save=False)
        instance.b.delete(save=False)
        instance.c.delete(save=False)
        instance.d.delete(save=False)
    except:
        pass



@receiver(pre_save, sender=tbloptionblki)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """


    try:
        old_img1 = instance.__class__.objects.get(id=instance.id).a.path
        old_img2 = instance.__class__.objects.get(id=instance.id).b.path
        old_img3 = instance.__class__.objects.get(id=instance.id).c.path
        old_img4 = instance.__class__.objects.get(id=instance.id).d.path

        try:
            new_img1 = instance.a.path

        except:
            new_img1 = None



        try:
            new_img2 = instance.b.path

        except:
            new_img2 = None



        try:
            new_img3= instance.c.path

        except:
            new_img3 = None



        try:
            new_img4 = instance.d.path

        except:
            new_img4 = None




        if new_img1 != old_img1:
            import os
            if os.path.exists(old_img1):
                os.remove(old_img1)



        if new_img2 != old_img2:
            import os
            if os.path.exists(old_img2):
                os.remove(old_img2)


        
        if new_img3 != old_img3:
            import os
            if os.path.exists(old_img3):
                os.remove(old_img3)

                        

        if new_img4 != old_img4:
            import os
            if os.path.exists(old_img4):
                os.remove(old_img4)




    except:
        pass



class tblansblk(models.Model):
    qstn = models.ForeignKey(tblblockquestion, related_name='blkqst')
    ans = models.CharField('Answer', max_length=75)
    option = models.CharField('Option', max_length=7500,default=0)

    def __unicode__(self):
        return u' a : %s, b:  %s ' % (self.ans, self.option)






class tblothers(models.Model):
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    term = models.CharField('Term',max_length=10)
    klass = models.CharField('Class', max_length=20)
    subject = models.CharField('Subject', max_length=75)
    exam_type = models.CharField('Exam Type', max_length=375)    
    qstcode = models.CharField('Code', max_length=20,default=0)
    q1 = models.CharField('Question', max_length=975)
    image = models.ImageField('Image', upload_to='questions', null=True,blank=True,default='studentpix/user.png')


    def __unicode__(self):
        return '%s %s %s'%(self.exam_type,self.subject,self.q1)



@receiver(post_delete, sender=tblothers)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass



@receiver(pre_save, sender=tblothers)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """


    try:
        old_img1 = instance.__class__.objects.get(id=instance.id).image.path

        try:
            new_img1 = instance.image.path

        except:
            new_img1 = None

                        

        if new_img1 != old_img1:
            import os
            if os.path.exists(old_img1):
                os.remove(old_img1)

    except:
        pass

    


class tbloptionsothers(models.Model):
    qstn = models.ForeignKey(tblothers, related_name='Options')
    a = models.CharField('Option A', max_length=7500)
    b = models.CharField('Option B', max_length=7500)
    c = models.CharField('Option C', max_length=7500)
    d = models.CharField('Option D', max_length=7500)
    e = models.CharField('Option E', max_length=7500)


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)    
  


class tbloptionothersi(models.Model):
    qstn = models.ForeignKey(tblothers, related_name='Optioni')
    a = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    b = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    c = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    d = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    e = models.ImageField('Image', upload_to='questions',default='questions/user.png')


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)



@receiver(pre_save, sender=tbloptionothersi)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """


    try:
        old_img1 = instance.__class__.objects.get(id=instance.id).a.path
        old_img2 = instance.__class__.objects.get(id=instance.id).b.path
        old_img3 = instance.__class__.objects.get(id=instance.id).c.path
        old_img4 = instance.__class__.objects.get(id=instance.id).d.path

        try:
            new_img1 = instance.a.path

        except:
            new_img1 = None



        try:
            new_img2 = instance.b.path

        except:
            new_img2 = None



        try:
            new_img3= instance.c.path

        except:
            new_img3 = None



        try:
            new_img4 = instance.d.path

        except:
            new_img4 = None




        if new_img1 != old_img1:
            import os
            if os.path.exists(old_img1):
                os.remove(old_img1)



        if new_img2 != old_img2:
            import os
            if os.path.exists(old_img2):
                os.remove(old_img2)


        
        if new_img3 != old_img3:
            import os
            if os.path.exists(old_img3):
                os.remove(old_img3)

                        

        if new_img4 != old_img4:
            import os
            if os.path.exists(old_img4):
                os.remove(old_img4)

    except:
        pass



class tblansothers(models.Model):
    qstn = models.ForeignKey(tblothers, related_name='Transaction')
    ans = models.CharField('Answer', max_length=75)
    option = models.CharField('Option', max_length=7500,default=0)

    def __unicode__(self):
        return u' a : %s, b:  %s ' % (self.ans, self.option)




class cbttimestable(models.Model):
    student = models.ForeignKey(Student, max_length=75)
    subject = models.CharField('Subject', max_length=25)
    start_time  = models.TimeField('Start Time', max_length=9)
    additional = models.CharField('Extend By', max_length=25,default=0)
    exam_type = models.CharField('Exam_type', max_length=75)
    term = models.CharField('Term',max_length=10, default=0)
    duration = models.CharField('Time', max_length=3)
    elapsed = models.CharField('Time', max_length=3)
    remaining = models.CharField('Time', max_length=3)

    def __unicode__(self):
        return u'%s-%s-%s-%s' %(self.exam_type,self.subject,self.student,self.term)
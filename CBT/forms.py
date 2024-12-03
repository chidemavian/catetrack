from django import forms
from setup.models import *
from sysadmin.models import *
from student.models import *
from lesson.models import *
from CBT.models import *


def sess():
    return currentsession.objects.get(id = 1)

sess = currentsession.objects.get(id = 1)
exam = (('Welcome back', 'Welcome back'),('Mid Term Exam', 'Mid Term Exam'),('Ca2' , 'Ca2'),('End Term Exam', 'End Term Exam'))



class subform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    email = forms.CharField(label = "E-mail",max_length = 20,required = True,widget = forms.TextInput())
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])


    def __init__(self, *args, **kwargs):
        super(subform, self).__init__(*args)
        self.fields['email'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'


class printform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.all()])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    exam_type = forms.ChoiceField(label= 'Exam Type', choices = [(r.exam_type, r.exam_type) for r in tblcbtexams.objects.all()])

    def __init__(self, *args):
        super(printform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        # self.fields['reporttype'].choices = [(a.reportsheet, a.reportsheet) for a in tblreportsheet.objects.filter(status = 'ACTIVE')]



class assessmentform(forms.Form):
    assess = forms.ChoiceField(label='Assessment Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.all()])
    status = forms.ChoiceField(label='Status',choices=( ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')))



class stuform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess)
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    exam_type = forms.ChoiceField(label='Exam Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.all()])
    def __init__(self, *args):
        super(stuform, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')




class formactive(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess)
    sfrom = forms.ChoiceField(label='From',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    sto = forms.ChoiceField(label='To',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices = [(c.term, c.term) for c in tblterm.objects.filter(status='ACTIVE')])
    exam_type = forms.ChoiceField(label='Exam Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.filter(status='ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    # duration = forms.CharField(label='Duration',max_length= 190,required=True)
    # st_date = forms.CharField(label='Date',max_length= 190,required=True,widget= forms.TextInput(attrs ={'readonly':'readonly'}))
    # st_time = forms.CharField(label='Start Time',max_length= 190,required=True)

    def __init__(self, *args):
        super(formactive, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'


class qstnform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'readonly':'readonly'}),initial=sess)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    subject=forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    term = forms.ChoiceField(label='Term',choices = [(c.term, c.term) for c in tblterm.objects.filter(status= 'ACTIVE')])
    exam_type = forms.ChoiceField(label='Exam Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.all()])
    question = forms.CharField(label= 'Question', max_length= 99190)
    pix = forms.ImageField(required=False,widget=forms.FileInput(attrs={'size':'5'}),label='Student Picture')
    


    def __init__(self, *args):
        super(qstnform, self).__init__(*args)
        self.fields['session'].choices = [(c.session, c.session) for c in currentsession.objects.filter(id = 1)]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]



class theoryform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'readonly':'readonly'}),initial=sess)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    subject=forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    term = forms.ChoiceField(label='Term',choices = [(c.term, c.term) for c in tblterm.objects.filter(status= 'ACTIVE')])
    exam_type = forms.ChoiceField(label='Exam Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.all()])
    
    pix = forms.ImageField(widget=forms.FileInput(attrs={'size':'5'}),label='Upload question image')
    
    # qimage = forms.ImageField('Theory File', upload_to='question')

    def __init__(self, *args):
        super(theoryform, self).__init__(*args)
        self.fields['session'].choices = [(c.session, c.session) for c in currentsession.objects.filter(id = 1)]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]




class compform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'readonly':'readonly'}),initial=sess)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    subject=forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    term = forms.ChoiceField(label='Term',choices = [(c.term, c.term) for c in tblterm.objects.filter(status= 'ACTIVE')])
    exam_type = forms.ChoiceField(label='Exam Type',choices = [(a.exam_type, a.exam_type) for a in tblcbtexams.objects.all()])
    


    def __init__(self, *args):
        super(compform, self).__init__(*args)
        self.fields['session'].choices = [(c.session, c.session) for c in currentsession.objects.filter(id = 1)]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]




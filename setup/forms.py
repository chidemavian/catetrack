from django import forms
from business.models import *



class ClassForm2(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    location = forms.ChoiceField(label='Location',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    subsection = forms.ChoiceField(label='Subsection',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    
    def __init__(self, *args):
        super(ClassForm2, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()
        self.fields['location'].choices = [(a.branch_code,a.address,) for a in tblbranch.objects.filter()]
        self.fields['location'].initial = tblbranch.objects.filter()




class Classroomform(forms.Form):#note that is this CA term that need to come from back end
    
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    subsection = forms.ChoiceField(label='Subsection',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    stream = forms.ChoiceField(label='Stream',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])    
    def __init__(self, *args):
        super(Classroomform, self).__init__(*args)



class gradingform(forms.Form):#note that is this CA term that need to come from back end
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    subsection = forms.ChoiceField(label='Subsection',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    def __init__(self, *args):
        super(gradingform, self).__init__(*args)


class subjectform(forms.Form):#note that is this CA term that need to come from back end
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    subsection = forms.ChoiceField(label='Subsection',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    department = forms.ChoiceField(label='Subject Category',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])    
    def __init__(self, *args):
        super(subjectform, self).__init__(*args)




class affectiveform(forms.Form):#note that is this CA term that need to come from back end
    
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    
    def __init__(self, *args):
        super(affectiveform, self).__init__(*args)
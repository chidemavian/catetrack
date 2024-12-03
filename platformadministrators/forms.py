
from django import forms

from business.models import *


class schoolform(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    

    def __init__(self, *args):
        super(schoolform, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()



class sectionform(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    location = forms.ChoiceField(label='Location',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])

    def __init__(self, *args):
        super(sectionform, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()
        self.fields['location'].choices = [(a.branch_code,a.address,) for a in tblbranch.objects.filter()]
        self.fields['location'].initial = tblbranch.objects.filter()



class selectappform(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    location = forms.ChoiceField(label='Location',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    

    def __init__(self, *args):
        super(selectappform, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()
        self.fields['location'].choices = [(a.branch_code,a.address,) for a in tblbranch.objects.filter()]
        self.fields['location'].initial = tblbranch.objects.filter()



class subsectionform(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    location = forms.ChoiceField(label='Location',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])

    def __init__(self, *args):
        super(subsectionform, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()
        self.fields['location'].choices = [(a.branch_code,a.address,) for a in tblbranch.objects.filter()]
        self.fields['location'].initial = tblbranch.objects.filter()


class streamform(forms.Form):#note that is this CA term that need to come from back end
  
    client = forms.ChoiceField(label='Client',choices = [( c.school_code,c.name) for c in tblschool.objects.all()])
    location = forms.ChoiceField(label='Location',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    section = forms.ChoiceField(label='Section',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    subsection = forms.ChoiceField(label='Subsection',choices=[( a.branch_code,a.address) for a in tblbranch.objects.filter()])
    # subsection = forms.ChoiceField(label='Subsection',choices=[( a.subsection.subsection,a.subsection.subsection) for a in tblbusinesssubsections.objects.filter()])
    def __init__(self, *args):
        super(streamform, self).__init__(*args)
        self.fields['client'].choices = [( c.school_code,c.name) for c in tblschool.objects.all()]
        self.fields['client'].initial = tblschool.objects.all()
        self.fields['location'].choices = [(a.branch_code,a.address,) for a in tblbranch.objects.filter()]
        self.fields['location'].initial = tblbranch.objects.filter()

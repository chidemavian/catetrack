from django import forms



class parentForm(forms.Form):
    surnam=forms.CharField(max_length=1)






class StudentRegisterForm(forms.Form):
    admitted_session = forms.CharField(max_length=12, label='Session', widget=forms.TextInput(attrs={'readonly': 'readonly'}))#,initial=sess)
    firstname = forms.CharField(label='First Name', max_length=75)
    surname = forms.CharField(label= 'Surname', max_length=75)
    othername = forms.CharField(label= 'Other Names', max_length=75,required=False)
    address = forms.CharField(label= 'Address', max_length=200,required=False,widget=forms.Textarea(attrs={'cols':'30','rows':'1'}))
    gender = forms.ChoiceField(label= 'Gender', choices=(('Male', 'Male'),('Female', 'Female')))
    studentpicture = forms.ImageField(required=False,widget=forms.FileInput(attrs={'size':'5'}),label='Student Picture')
    

    def __init__(self, *args):
        super(StudentRegisterForm, self).__init__(*args)

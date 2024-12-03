# Create your views here.
from django.core.serializers.json import json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from setup.models import *
from student.models import *
from student.forms import *

from platformowners.utils import *

#from student.utils import render_to_pdf, render_to_xls

from sysadmin.admin import *
from academics.models import *
from sysadmin.models import *



import datetime
from datetime import date
import xlwt
import random




def autocomplete(request):
    term = request.GET.get('term')
    #p =  request.GET.get('query')
    #print p
    qset = Student.objects.filter(fullname__contains=term,admitted_session = sessi,gone = False)[:10]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    return suggestions


def index(request):
    return render_to_response('student/base.html', {})

def wel(request):

    if  "userid" in request.session:
        varuser=request.session['userid']
        user = ratifyuser(varuser)
        
        return render_to_response('student/wel.html',{
            'varuser':user['varuser'],
            'company':user['company'],
            'pincode':user['pincode']}) 


        return render_to_response('student/wel.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')



def wecl(request): #js 3 to ss 1
    if  "userid" in request.session:

          varuser=request.session['userid']

          oldsession = '2022/2023'
          sessionnew = '2023/2024'

          subklass='Science'
          arm='SCIENCE'

          llist=['BFC/21/0240/2869','BFC/21/0268/2892','BFC/21/0242/4607','BFC/22/0379/7128',
          'BFC/21/0262/5146','BFC/21/0231/3933','BFC/21/0245/7738','BFC/21/0275/8889',
          'BFC/21/0249/3146','BFC/21/0287/0466','BFC/21/0385/9007','BFC/21/0237/2562','BFC/21/0373/6247',
          'BFC/21/0369/3025','BFC/21/0246/1874','BFC/21/0218/7348','BFC/22/0373/2064']


          for jn in llist:
            kk = Student.objects.get(admitted_session=oldsession,gone=0,admissionno=jn )

            Student(birth_date= kk.birth_date,
                admitted_session = sessionnew,
                first_term = True, 
                second_term = True, 
                third_term = True,
                firstname = kk.firstname,
                surname = kk.surname,
                othername = kk.othername,
                address = kk.address,
                sex = kk.sex,
                birth_place = kk.birth_place,
                state_of_origin =kk.state_of_origin,
                lga = kk.lga,
                fathername =kk.fathername,
                fatheraddress = kk.fatheraddress,
                fathernumber = kk.fathernumber,
                fatheroccupation =kk.fatheroccupation,
                fatheremail = kk.fatheremail,
                prev_school =kk.prev_school,
                prev_class = kk.prev_class,
                admitted_class = 'SS 1',
                admitted_arm = arm,
                admissionno = kk.admissionno,
                house = kk.house,
                dayboarding = kk.dayboarding,
                subclass = subklass,
                userid = varuser,
                studentpicture = kk.studentpicture).save() #takenote



            newstu = Student.objects.get(admitted_session=sessionnew,gone=0,admissionno=jn)


            terrm = ['First', 'Second', 'Third']
            for term in terrm:
                StudentAcademicRecord(student=newstu,term=term,session=sessionnew).save()

                co = StudentAcademicRecord.objects.get(student=newstu, term = term)

                AffectiveSkill(academic_rec=co).save()
                PsychomotorSkill(academic_rec=co).save()

               #counts no of subjects
                P = Subject.objects.filter(category = subklass).count()
                P = P+1
                for n in range (1,P):
                    sub = Subject.objects.get(category = subklass, num = n)
                    if sub.category2 == 'Compulsory':

                        SubjectScore(academic_rec = co,                                    
                            subject = sub.subject, 
                            num = n, 
                            klass = newstu.admitted_class, 
                            session = sessionnew, 
                            arm = newstu.admitted_arm, 
                            term = term).save()

      # Migrationhistory.objects.all().delete()

    succ = "Successful !!!"
    return render_to_response('student/wel.html',{'varuser':varuser})
       




def weluu(request): #delete reg
    term=['First','Second','Third']
    admissionno='BFC/22/0420/4814'

    k = Student.objects.get(admissionno=admissionno)
    for t in term:
        p=StudentAcademicRecord.objects.filter(student=k,term=t)
        score= SubjectScore.objects.filter(academic_rec=p)
        affec=AffectiveSkill.objects.filter(academic_rec=p)
        psy= PsychomotorSkill.objects.filter(academic_rec=p)

        p.delete()
        score.delete()
        affec.delete()
        psy.delete()

    k.delete()


def welcd(request): #swap classroom for second and third term


    terrm=['First','Second','Third']

  # for kj in armss:
    gh =Student.objects.all()
    for k in gh:
      k.surname.lower()
      k.save()
      k.firstname.lower()
      k.save()
      k.othername.lower()
      k.save()







def welam(request): #swap classroom

    armss=['COMMERCIAL','SCIENCE','ART']
    terrm=['First','Second','Third']

  # for kj in armss:
    gh =Student.objects.get(admitted_session='2022/2023',admissionno='BFC/22/036/7244', admitted_arm='A',gone =0)

    for tt in terrm:
      vg = StudentAcademicRecord.objects.get(student=gh,term = tt)
      ll= SubjectScore.objects.filter(term=tt,academic_rec=vg).update(arm='B')
      vg.arm='B'
      vg.save()
    gh.admitted_arm='B'

    gh.save()
      



def wwelsbj(request): #assign sub

    armss=['COMMERCIAL','SCIENCE','ART']
    terrm=['First','Second','Third']

  # for kj in armss:
    gh =Student.objects.filter(admitted_session='2022/2023',admitted_arm='SCIENCE',gone =0)
    nb = Subject.objects.get(category='Science',subject='AGRICULTURAL SCIENCE')

    for k in gh:
      for tt in terrm:
        vg = StudentAcademicRecord.objects.get(student=k,term = tt)
        try:
          SubjectScore.objects.get(term=tt,subject='AGRICULTURAL SCIENCE',academic_rec=vg)
        except:
          SubjectScore(academic_rec = vg,
            subject = 'AGRICULTURAL SCIENCE', 
            num = nb.num, 
            klass = k.admitted_class,
            session = '2022/2023', 
            arm = k.admitted_arm,
            term = tt).save()





def wwelels(request): #assign TD


    terrm=['First','Second','Third']
    
    km =[ 'BFC/21/0348/5380','BFC/21/0290/7363','BFC/21/0307/3616',
          'BFC/21/0304/6985','BFC/22/0371/0405']

    for m in km :
      k =Student.objects.get(admitted_session='2022/2023',
        admissionno=m, 
        admitted_class='SS 1', 
        admitted_arm='SCIENCE',
        gone =0)

      nb = Subject.objects.get(category='Science',subject='T.D')

      for tt in terrm:
        vg = StudentAcademicRecord.objects.get(student=k,term = tt)
        try:
          SubjectScore.objects.get(term=tt,subject='T.D',academic_rec=vg)
        except:
          SubjectScore(academic_rec = vg,
            subject = 'T.D', 
            num = nb.num, 
            klass = k.admitted_class,
            session = '2022/2023', 
            arm = k.admitted_arm,
            term = tt).save()


def wwelkat(request): #assign catering

    terrm=['First','Second','Third']
    
    km =[ 
            #comm
              # 'BFC/21/0065/3371',
              # 'BFC/21/0067/6480',
              'BFC/21/0068/8925',
              # 'BFC/21/0078/5227',
              # 'BFC/21/0073/6669',
              # 'BFC/21/0074/1433',
              # 'BFC/21/0076/4338',


            ]

    subject = 'AGRICULTURAL SCIENCE'

    for m in km :
      k =Student.objects.get(admitted_session='2022/2023',
        admissionno=m,
        gone =0)

      if k.admitted_arm == 'COMMERCIAL':
        kat= 'Commercial'
      elif k.admitted_arm == 'SCIENCE':
        kat = 'Science'


      nb = Subject.objects.get(category=kat,subject=subject)

      for tt in terrm:
        vg = StudentAcademicRecord.objects.get(student=k,term = tt)
        try:
          SubjectScore.objects.get(term=tt,subject=subject,academic_rec=vg)
        except:
          SubjectScore(academic_rec = vg,
            subject = subject, 
            num = nb.num, 
            klass = k.admitted_class,
            session = '2022/2023', 
            arm = k.admitted_arm,
            term = tt).save()


def wwelsub(request): #sync subclass with arm

    armss=['COMMERCIAL','SCIENCE','ART']
    terrm=['First','Second','Third']

    for kj in armss:
      gh =Student.objects.filter(admitted_session='2022/2023',admitted_arm=kj,gone =0)

      for k in gh:
        if kj == 'ART':
          k.subclass='Art'

        elif kj == 'SCIENCE':
          k.subclass='Science'
        elif kj == 'COMMERCIAL':
          k.subclass='Commercial'
        k.save()

        
        if kj == 'ART':
          nb = Subject.objects.get(category='Art',subject='CRS')
          for tt in terrm:
            vg = StudentAcademicRecord.objects.get(student=k,term = tt)
            try:
              SubjectScore.objects.get(term=tt,subject='CRS',academic_rec=vg)
            except:
              SubjectScore(academic_rec = vg,
                subject = 'CRS', 
                num = nb.num, 
                klass = k.admitted_class,
                session = '2022/2023', 
                arm = k.admitted_arm,
                term = tt).save()


def wwelart(request): #to switch from science to art dept

    gh=['BFC/21/0326/5615',
    'BFC/21/0295/8294',
    'BFC/21/0334/6251',
    'BFC/21/0324/5923',
    'BFC/21/0323/5105',
    'BFC/21/0300/7375',
    'BFC/21/0309/2398',
    'BFC/21/0310/4583',
    'BFC/21/0312/8031',
    'BFC/21/0306/2947',
    'BFC/21/0329/8768',
    'BFC/21/0366/0473',
    'BFC/21/0293/0068',
    'BFC/21/0333/8769',
    'BFC/21/0320/3162',
    'BFC/21/0311/0762',
    'BFC/21/0315/4114',
    'BFC/21/0356/8726',
    'BFC/21/0297/7290']

    terrm=['First','Second','Third']

    for k in gh:
      dlp = Student.objects.get(admissionno=k,
        admitted_class='SS 1', 
        admitted_session='2022/2023',
        gone=0)

      dlp.admitted_arm='ART'
      dlp.save()

      for tt in terrm:
        vg = StudentAcademicRecord.objects.get(student=dlp,term = tt)
        vg.arm='ART'
        vg.save()

        ss = SubjectScore.objects.filter(academic_rec=vg, term = tt).delete()

        P = Subject.objects.filter(category = 'Art').count()
        P = P+1
        for n in range (1,P):
            sub = Subject.objects.get(category = 'Art', num = n)
            if sub.category2 == 'Compulsory':
                SubjectScore(academic_rec = vg,
                  subject = sub.subject, 
                  num = n, 
                  klass = 'SS 1', 
                  session = '2022/2023', 
                  arm = 'ART', 
                  term = tt).save()




def wwelcommerce(request): #to switch from science to art dept

    gh=['BFC/21/0319/7580',
    'BFC/21/0346/4635',
    'BFC/21/0321/1299',
    'BFC/21/0342/6182',
    'BFC/21/0358/9678',
    'BFC/21/0344/8323',
    'BFC/21/0301/5308',
    'BFC/21/0355/2476']

    terrm=['First','Second','Third']

    for k in gh:
      dlp = Student.objects.get(admissionno=k,
        admitted_class='SS 1', 
        admitted_session='2022/2023',
        gone=0)

      dlp.admitted_arm='COMMERCIAL'
      dlp.save()

      for tt in terrm:
        vg = StudentAcademicRecord.objects.get(student=dlp,term = tt)
        vg.arm='COMMERCIAL'
        vg.save()

        ss = SubjectScore.objects.filter(academic_rec=vg, term = tt).delete()

        P = Subject.objects.filter(category = 'Commercial').count()
        P = P+1
        for n in range (1,P):
            sub = Subject.objects.get(category = 'Commercial', num = n)
            if sub.category2 == 'Compulsory':
                SubjectScore(academic_rec = vg,
                  subject = sub.subject, 
                  num = n, 
                  klass = 'SS 1', 
                  session = '2022/2023', 
                  arm = 'COMMERCIAL', 
                  term = tt).save()








def wellp(request): #check doeble reg 

    k = Student.objects.filter(admitted_session='2021/2022')
    st=[]
    for h in k:
      fn = h.fullname
      nt = Student.objects.filter(fullname=fn).count()
      if nt>1:
        adm=h.admissiono
        st.append(adm)

    msg =st
    return render_to_response('student/selectloan.html',{'msg':msg})



def welkpa(request): #letter_new student
    t = Student.objects.filter(gone =0,admitted_session='2022/2023').order_by('admitted_class','admitted_arm')
    stu=[]
    slt=[]
    for k in t:
      adm = k.admissionno
      a,b,c,r=adm.split('/')
      if b == '22':
        stu.append(k)


    for l in stu:
      adm = l.admissionno
      surname=l.surname.upper()

      if l.sex == 'Female':
        gender = 'her'
      else:
        gender='him'
      kk ={'student':l,'gender':gender,'surname':surname}

      slt.append(kk)
    return render_to_response('letter_new.html',{'st':slt})


def welkm(request): #letter_all student
    t = Student.objects.filter(gone =0).order_by('admitted_class','admitted_arm')
    stu=[]
    for k in t:
      adm = k.admissionno
      surname=k.surname
      surname=surname.upper()

      if k.sex == 'Female':
        gender = 'her'
      else:
        gender='his'
      kk ={'student':k,'gender':gender,'surname':surname}

      stu.append(kk)
    return render_to_response('letter.html',{'st':stu})


def welbn(request): #letter
    k =['ACCOUNTING', 'CRS','FINE ART', 'GOVERNMENT']
    # k =['ACCOUNTING', 'COMMERCE', 'CRS','FINE ART', 'GOVERNMENT']
    for k in k:
      g= Subject.objects.get(category='Science', subject=k)
      g.delete()

def welbn(request): #renumber num
    g= Subject.objects.get(category='Science', num=18, subject='FOOD NUTRITION', category2='Optional')
    g.num=15
    g.save()


def welp(request): #rewrite admission no
  k = Student.objects.filter(gone=False, admitted_session='2021/2022')
  for  j in k:

    k = random.randint(0,9)
    y = random.randint(0,9)
    x = random.randint(0,9)
    z = random.randint(0,9)
    a = random.randint(0,9)

    pin =  str(k) + str(y) + str(x) + str(z)
    A,B,C = j.admissionno.split('/') 
    kk = 'BFC/%s/%s/%s/%s'%(A,B,C,pin)
    j.admissionno=kk
    j.save()

def welbu(request): #rewrite subject label
    g= Subject.objects.get(category='Science', 
      subject='F/MATHS', 
      category2='Compulsory')
    g.subject= 'FURTHER MATHS'
    g.save()

    st = subjectteacher.objects.filter(session='2021/2022',subject='F/MATHS').update(subject='FURTHER MATHS')
    sc = SubjectScore.objects.filter(subject='F/MATHS').update(subject='FURTHER MATHS')


def welb(request): #reportsheet calc
  k1=['JS 1', 'JS 2','JS 3']
  a1 =['A','B','C']
  k2=['SS 1', 'SS 2','SS 3']
  a2=['SCIENCE','COMMERCIAL','ART']
  session='2021/2022'
  term='Second'
  for klass in k1:
    for arm in a1:
      ttt =Student.objects.filter(admitted_class=klass,admitted_arm=arm)
      for s in ttt:
        admno=s.admissiono
        sa=studentaveragemid(admno,term,session,klass,arm)

      sub=subjectaveragemid(term,session,klass,arm) #class stat
      ca=classaveragemid(admno,klass,session,term,arm)#class stat



def yesno(request):
    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:
            form = StudentRegisterForm()

            if request.method == 'POST':
              g=9

            else:
              if user['branch'].company.business_type.id ==1:

                return render_to_response('student/yesno.html', {
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})
              
              else:
                return render_to_response('student/register.html',{
                      'varuser':user['varuser'],
                      'form': form,
                      'company':user['company'],
                      'pincode':user['pincode']})



    else:
        return HttpResponseRedirect('/login/')


def registerw(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = ratifyuser(varuser)
        
        if user['admin']:



          varerr =''
          form = StudentRegistrationForm()
          if request.method == 'POST':
             form = StudentRegistrationForm(request.POST, request.FILES)
             if form.is_valid():
                 birth_date= form.cleaned_data['birth_date']
                 admitted_session = form.cleaned_data['admitted_session']
                 
                 firstname1 = form.cleaned_data['firstname']
                 firstname1=firstname1.lower()

                 surname1 = form.cleaned_data['surname']
                 surname1=surname1.lower()

                 othername1 =  form.cleaned_data['othername']
                 othername1=othername1.lower()
                 
                 address = form.cleaned_data['address']
                 sex = form.cleaned_data['sex']
                 birth_place = form.cleaned_data['birth_place']
                 state_of_origin = form.cleaned_data['state_of_origin']
                 lga = form.cleaned_data['lga']
                 fathername = form.cleaned_data['fathername']
                 fatheraddress = form.cleaned_data['fatheraddress']
                 fathernumber =  form.cleaned_data['fathernumber']
                 fatheroccupation = form.cleaned_data['fatheroccupation']
                 fatheremail = form.cleaned_data['fatheremail']
                 prev_school =  form.cleaned_data['prev_school']
                 prev_class =  form.cleaned_data['prev_class']
                 admitted_class = form.cleaned_data['admitted_class']
                 admitted_arm = form.cleaned_data['admitted_arm']
                 admissionno1 = form.cleaned_data['admissionno']
                 house = form.cleaned_data['house']
                 dayboarding = form.cleaned_data['dayboarding']
                 subclass = form.cleaned_data['subclass']
                 rfile = form.cleaned_data['studentpicture']
                 getf = str(firstname1)
                 getf1 = str(surname1)
                 getf2 = str(othername1)
                 getf3 = str(admissionno1)
                 firstname = getf.replace(':','')
                 surname = getf1.replace(':','')
                 othername = getf2.replace(':','')
                 admissionno = getf3.replace(':','')
                 admissionno = admissionno.upper()
                 adm = admissionno
                 spadm = admitted_session
                 j,k = spadm.split("/")
                 js = int(k)
                 js += 1
                 newsession = k + '/' + str(js)
                 if rfile is None:
                     studentpicture = 'studentpix/user.png'
                 else:
                     studentpicture = request.FILES['studentpicture']

                 if Student.objects.filter(admissionno = admissionno).count()  > 0:
                  varerr = "Admission No IN EXISTENCE"
                  return render_to_response('student/register.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))

                 today = datetime.datetime.now()
                 tm = today.month

                 if tm == 9 or tm == 10 or tm == 11 or tm == 12:
                     Student(birth_date= birth_date,admitted_session = admitted_session,first_term = True, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture).save()
                 if tm == 1 or tm == 2 or tm == 3 or tm == 4:
                     Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture).save()
                 if tm == 5 or tm == 6 or tm == 7 or tm == 8:
                     Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = False, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture).save()
                 fullname = str(surname) + ' ' + str(firstname) + ' '+ str(othername)



                 today = datetime.datetime.now()
                 tm = today.month
                 akrec = Student.objects.get(admissionno = admissionno, admitted_session = admitted_session)

       

                 if tm == 9 or tm == 10 or tm == 11 or tm == 12 and admitted_session == admitted_session:
                     terrm = ['First', 'Second', 'Third']
                     for term in terrm:
                         akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                         akademics.save()
                         AffectiveSkill(academic_rec=akademics).save()
                         PsychomotorSkill(academic_rec=akademics).save()
                         co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                         #counts no of subjects
                         P = Subject.objects.filter(category = akrec.subclass).count()
                         P = P+1
                         for n in range (1,P):
                             sub = Subject.objects.get(category = akrec.subclass, num = n)
                             if sub.category2 == 'Compulsory':
                                 SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()




                 if tm == 1 or tm == 2 or tm == 3 or tm == 4 :#and session == admitted_session:
                     terrm2 = ['Second','Third']
                     for term in terrm2:
                         akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                         akademics.save()
                         AffectiveSkill(academic_rec=akademics).save()
                         PsychomotorSkill(academic_rec=akademics).save()
                         co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                         P = Subject.objects.filter(category =akrec.subclass ).count()
                         P = P+1
                         for n in range (1,P):
                             sub = Subject.objects.get(category = akrec.subclass, num = n)
                             if sub.category2 == 'Compulsory':
                                 SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()
                 
   

                 
                 if tm == 5 or tm == 6 or tm == 7 or tm == 8 and admitted_session == admitted_session:
                     terrm3 = ['Third']
                     for term in terrm3:
                         akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                         akademics.save()
                         AffectiveSkill(academic_rec=akademics).save()
                         PsychomotorSkill(academic_rec=akademics).save()
                         co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                         P = Subject.objects.filter(category=akrec.subclass).count()
                         P = P+1
                         for n in range (1,P):
                             sub = Subject.objects.get(category = akrec.subclass, num = n)
                             if sub.category2 == 'Compulsory':
                                 SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()
   



                 try:
                     used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                     used.save()
                 except :
                     pass
                 if dayboarding == 'Boarding':
                     try:

                         used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                         used.save()
                         used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                         used.save()
                     except :
                         return HttpResponseRedirect('/student/success/')
                 else:
                     return HttpResponseRedirect('/student/success/')
             

             else:
                varerr = "All Fields Are Required"
                return render_to_response('student/register.html',{
                      'varuser':user['varuser'],
                      'form': form,
                      'company':user['company'],
                      'pincode':user['pincode']})

          else:
            k= user['branch'].company.business_type

            if k.id ==1:
              return render_to_response('student/register.html',{
                    'varuser':user['varuser'],
                    'form': form,
                    'company':user['company'],
                    'pincode':user['pincode']})
            elif k.id ==2:
              return HttpResponseRedirect('/welcome/')
        else:
          return HttpResponseRedirect('/welcome/')


    else:
        return HttpResponseRedirect('/login/')


def register_og(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = ratifyuser(varuser)
        
        if user['admin']:
          varerr =''
          form = parentForm()
          if request.method == 'POST':
            form = parentForm(request.POST, request.FILES)
            if form.is_valid():
              firstname1 = form.cleaned_data['firstname'].lower()

              surname1 = form.cleaned_data['surname'].lower()

              othername1 =  form.cleaned_data['othername'].lower()

              address = form.cleaned_data['address']

              fathername = form.cleaned_data['fathername']
              fatheraddress = form.cleaned_data['fatheraddress']
              fathernumber =  form.cleaned_data['fathernumber']
              fatheroccupation = form.cleaned_data['fatheroccupation']
              fatheremail = form.cleaned_data['fatheremail']
              return HttpResponseRedirect('/student/success/')
            else:
                 return HttpResponseRedirect('/student/success/')
           

          else:
            varerr = "All Fields Are Required"
            return render_to_response('student/parent.html',{
                  'varuser':user['varuser'],
                  'form': form,
                  'company':user['company'],
                  'pincode':user['pincode']})
      
        else:
          return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')




def getlocal(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print nation,state
                kk = [] #empty dictionary
                data = LGA.objects.filter(state = state).order_by('lga')
                for p in data:
                    kk.append(p.lga)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
"""
#def getadmno(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print 'the post :',state
                currr = state.split('/')[0]
                dd = []
                if Student.objects.filter().count() == 0 :
                    stno = 0
                else:
                    sdata = Student.objects.filter(admitted_session = state)
                    for j in sdata:
                        sno = j.admissionno
                        curr = sno.split('/')[1]
                        currb= int(curr)
                        dd.append(currb)
                    dd.sort(reverse= True)
                    stno = dd[0]
                stnno = int(stno)
                stnno1 = stnno + 1
                tday = datetime.date.today()
                ty = tday.year
                typ = str(ty)
                tyy = typ[2:]
                #kk = 'SCS/%s/%.4d'%(tyy, stnno1)
                #data = Student.objects.filter(admitted_session = state).count()
                #data +=  1
                #kk = 'SCS/%s/%.4d'%(currr[2:], stnno1) For Skylink
            #    kk = 'LC/%.4d'%stnno1
                kk = 'AC/SEC/%.4d/%s'%(stnno1, tyy)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
"""



def getadmno(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print 'the post :',state
                currr = state.split('/')[0]
                dd = []
                if Student.objects.filter(admitted_session=currse).count() == 0 :
                    stdno = 0
                else:
                    sdata = Student.objects.filter(admitted_session = state)
                    for j in sdata:
                        sno = j.admissionno
                        curr = sno.split('/')[1]
                        currb= int(curr)
                        dd.append(currb)
                    dd.sort(reverse= True)
                    stdno = dd[0]
                stnno = int(stdno)
                stnno1 = stnno + 1
                tday = datetime.date.today()
                ty = tday.year
                typ = str(ty)
                tyy = typ[2:]

                k = random.randint(0,9)
                y = random.randint(0,9)
                x = random.randint(0,9)
                z = random.randint(0,9)
                a = random.randint(0,9)

                pin =  str(k) + str(y) + str(x) + str(z)

                if Student.objects.filter(admitted_session=currse).count() == 0 :
                    data = 1
                else:
                    data = Student.objects.filter(admitted_session = state).count()
                    data +=  1
                # kk = '%s/%s/%s/%s'%(A,B,C,pin)
                reg = 'BFC/%s/%.4d/%s'%(currr[2:], data,pin)
                #kk = 'AC/%s/%.4d'%(currr[2:], stnno1) #For Skylink
                #kk = 'AC/%.4d'%stnno1
                return HttpResponse(json.dumps(reg), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubclass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                data = []
                kk = []
                if subclass.objects.filter(subcode = state):
                  data1 = subclass.objects.filter(subcode = state)
                  for j in data1:
                      data.append(j.classsub)
                else:
                    data.append('Nil')

                for p in data:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getstuinfoauto(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = Student.objects.get(admitted_class = klass,admitted_arm = arm,admitted_session = currse,fullname = stuname,admissionno = admno)
                return render_to_response('student/regform10.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/regform.html',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstuinfo(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm = acccode.split('-') #split must be same as whats in html
                kk = []
                data = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = currse,gone = False).order_by('fullname')
                for p in data:
                    jn = p.fullname+':'+p.admissionno
                    kk.append(jn)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def editreg(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.editregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        if request.method == 'POST':
                birth_date= request.POST['birth_date']
                admitted_session = request.POST['admitted_session']
                firstname1 = request.POST['firstname']
                surname1 = request.POST['surname']
                othername1 =  request.POST['othername']
                address = request.POST['address']
                sex = request.POST['sex']
                birth_place = request.POST['birth_place']
                state_of_origin = request.POST['state_of_origin']
                lga = request.POST['lga']
                fathername = request.POST['fathername']
                fatheraddress = request.POST['fatheraddress']
                fathernumber =  request.POST['fathernumber']
                fatheroccupation = request.POST['fatheroccupation']
                fatheremail = request.POST['fatheremail']
                prev_school =  request.POST['prev_school']
                prev_class =  request.POST['prev_class']
                admitted_class = request.POST['admitted_class']
                admitted_arm = request.POST['admitted_arm']
                admissionno1 = request.POST['admissionno']
                house = request.POST['house']
                dayboarding = request.POST['dayboarding']
                subclass = request.POST['subclass']
                admissionnoold = request.POST['admissionnoold']
                oldclass = request.POST['oldclass']
                oldarm = request.POST['oldarm']
                oldname = request.POST['oldname']
                getf = str(firstname1)
                getf1 = str(surname1)
                getf2 = str(othername1)
                getf3 = str(admissionno1)
                firstname = getf.replace(':','')
                surname = getf1.replace(':','')
                othername = getf2.replace(':','')
                admissionno = getf3.replace(':','')
                admissionno = admissionno.upper()
                if 'studentpicture' in request.FILES:
                    photo_file = request.FILES['studentpicture']
                    k1 = str(photo_file.name)
                    j = k1.split('.')[1]
                     #print k,j
                    if not (j.lower() in ['jpeg','jpg','png','bmp']):
                       varerr = "%s is not a required picture" % k1
                       getdetails = Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                       return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform})
                    else:
                       pass
                else:
                    gda =  Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                    # print gda.picture
                    photo_file = gda.studentpicture

                if Student.objects.filter(admissionno = admissionno).exclude(admissionno = admissionnoold).count() == 0:
                    pass
                else:
                    varerr = "Error in your request !! - Another Student with Admission No  %s IN EXISTENCE" %admissionno
                    return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
               
                # if  birth_date == "" or admitted_session == "" or firstname == "" or surname == "" or address == "" or birth_place == "" or fathername == "" or fatheraddress == "" or fatheroccupation == "" or   admissionno == "" :
                    # varerr = "ALL FIELDS ARE REQUIRED"
                    # return HttpResponseRedirect('/student/editregistration/')
                    # return render_to_response('student/edit_reg.html',{'varerr':varerr},context_instance = RequestContext(request))
                    # return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
                


                #getting the old student details
                #oldrecord = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                # getting class for the new class


                seldata = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                oldrec = seldata
                seldata. birth_date= birth_date
                seldata.address = address
                seldata.firstname = firstname
                seldata.surname = surname
                seldata.othername = othername
                seldata.address = address
                seldata.sex = sex
                seldata.birth_place = birth_place
                seldata.state_of_origin = state_of_origin
                seldata.lga = lga
                seldata.fathername =fathername
                seldata.fatheraddress= fatheraddress
                seldata.fathernumber = fathernumber
                seldata.fatheroccupation = fatheroccupation
                seldata.fatheremail = fatheremail
                seldata.prev_school = prev_school
                seldata.prev_class = prev_class
                seldata.admitted_class = admitted_class
                seldata.admitted_arm = admitted_arm
                seldata.admissionno = admissionno
                seldata.house = house
                seldata.dayboarding = dayboarding
                seldata.subclass = subclass
                seldata.userid = varuser
                seldata.studentpicture = photo_file #*******why pic doesnt update
                seldata.save()
                #*************************************
                spadm = admitted_session
                j,k = spadm.split("/")
                js = int(k)
                js += 1
                #here i need to update the academic records
                stacarec = StudentAcademicRecord.objects.filter(student = oldrec)
                StudentAcademicRecord.objects.filter(student = oldrec).update(arm = admitted_arm,klass = admitted_class)
                for k in stacarec:
                   SubjectScore.objects.filter(academic_rec = k).update(klass = admitted_class,arm = admitted_arm)
                # here i need to update the account table
                fullname =  str(surname) +' '+ str(firstname) + ' '+ str(othername)
                if tblaccount.objects.filter(acccode = admissionno):
                    getacc = tblaccount.objects.get(acccode = admissionno)
                    #getacc.acccode = admissionno
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = admissionnoold).update(acccode = admissionno,accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                    used.save()
                #updating the liabilities
                if tblaccount.objects.filter(acccode = 'L'+str(admissionno)):
                    getacc = tblaccount.objects.get(acccode = 'L'+str(admissionno))
                    #getacc.acccode = 'L'+str(admissionno)
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = 'L'+str(admissionnoold)).update(acccode = 'L'+str(admissionno),accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                    #used.save()
                #treating other liabilities
                if tblaccount.objects.filter(acccode = 'C'+str(admissionno)):
                    getacc = tblaccount.objects.get(acccode = 'C'+str(admissionno))
                    #getacc.acccode = 'C'+str(admissionno)
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = 'C'+str(admissionnoold)).update(acccode = 'C'+str(admissionno),accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                   # used.save()
                return HttpResponseRedirect('/student/success/')
        else:
            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/edit_reg.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')




def editbio(request):
    # fr = Student.objects.get(admitted_session='2022/2023',admissionno='BFC/21/0274/7952')
    # sn =fr.surname
    # fn =fr.firstname
    # on = fr.othername
    # gb = Student.objects.filter(admissionno='BFC/21/0274/7952').update(firstname=fn,surname=sn,othername=on)

    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.editregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        if request.method == 'POST':
                
                surname = request.POST['surname']
                othername =  request.POST['othername']
                firstname = request.POST['firstname']                
                address = request.POST['address']
                sex = request.POST['sex']

                birth_date= request.POST['birth_date']

                birth_place = request.POST['birth_place']

                state_of_origin = request.POST['state_of_origin']
                lga = request.POST['lga']

                oldclass = request.POST['oldclass']
                oldarm = request.POST['oldarm']
                oldname = request.POST['oldname']

                getf = str(firstname)
                getf1 = str(surname)
                getf2 = str(othername)
                admissionnoold = request.POST['admissionnoold']



                # admitted_session = request.POST['admitted_session']
                # fathername = request.POST['fathername']
                # fatheraddress = request.POST['fatheraddress']
                # fathernumber =  request.POST['fathernumber']
                # fatheroccupation = request.POST['fatheroccupation']
                # fatheremail = request.POST['fatheremail']
                # prev_school =  request.POST['prev_school']
                # prev_class =  request.POST['prev_class']
                # admitted_class = request.POST['admitted_class']
                # admitted_arm = request.POST['admitted_arm']
                # admissionno1 = request.POST['admissionno']
                # house = request.POST['house']
                # dayboarding = request.POST['dayboarding']
                # subclass = request.POST['subclass']             

                # getf3 = str(admissionno1)
                # firstname = getf.replace(':','')
                # surname = getf1.replace(':','')
                # othername = getf2.replace(':','')
                # admissionno = getf3.replace(':','')
                # admissionno = admissionno.upper()


                if 'studentpicture' in request.FILES:
                    photo_file = request.FILES['studentpicture']
                    k1 = str(photo_file.name)
                    j = k1.split('.')[1]
                     #print k,j
                    if not (j.lower() in ['jpeg','jpg','png','bmp']):
                       varerr = "%s is not a required picture" % k1
                       getdetails = Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                       return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform})
                    else:
                       pass
                else:
                    gda =  Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                    # print gda.picture
                    photo_file = gda.studentpicture



                if Student.objects.filter(admissionno = admissionnoold).exclude(admissionno = admissionnoold).count() == 0:
                    pass
                else:
                    varerr = "Error in your request !! - Another Student with Admission No  %s IN EXISTENCE" %admissionno
                    return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
          




                # if  birth_date == "" or admitted_session == "" or firstname == "" or surname == "" or address == "" or birth_place == "" or fathername == "" or fatheraddress == "" or fatheroccupation == "" or   admissionno == "" :
                    # varerr = "ALL FIELDS ARE REQUIRED"
                    # return HttpResponseRedirect('/student/editregistration/')
                    # return render_to_response('student/edit_reg.html',{'varerr':varerr},context_instance = RequestContext(request))
                    # return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
                


                #getting the old student details
                #oldrecord = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                # getting class for the new class


                seldata = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                oldrec = seldata
                
                seldata. birth_date= birth_date
                seldata.address = address
                seldata.firstname = firstname
                seldata.surname = surname
                seldata.othername = othername
                seldata.address = address
                seldata.sex = sex
                seldata.birth_place = birth_place
                seldata.state_of_origin = state_of_origin
                seldata.lga = lga

                # seldata.fathername =fathername
                # seldata.fatheraddress= fatheraddress
                # seldata.fathernumber = fathernumber
                # seldata.fatheroccupation = fatheroccupation
                # seldata.fatheremail = fatheremail
                # seldata.prev_school = prev_school
                # seldata.prev_class = prev_class
                # seldata.admitted_class = admitted_class
                # seldata.admitted_arm = admitted_arm
                # seldata.admissionno = admissionno
                # seldata.house = house
                # seldata.dayboarding = dayboarding
                # seldata.subclass = subclass
                # seldata.userid = varuser

                seldata.studentpicture = photo_file #*******why pic doesnt update
                seldata.save()

                # #*************************************
                # spadm = admitted_session
                # j,k = spadm.split("/")
                # js = int(k)
                # js += 1
                # #here i need to update the academic records
                # stacarec = StudentAcademicRecord.objects.filter(student = oldrec)
                # StudentAcademicRecord.objects.filter(student = oldrec).update(arm = admitted_arm,klass = admitted_class)
                # for k in stacarec:
                #    SubjectScore.objects.filter(academic_rec = k).update(klass = admitted_class,arm = admitted_arm)
                # # here i need to update the account table
                # fullname =  str(surname) +' '+ str(firstname) + ' '+ str(othername)
                # if tblaccount.objects.filter(acccode = admissionno):
                #     getacc = tblaccount.objects.get(acccode = admissionno)
                #     #getacc.acccode = admissionno
                #     getacc.accname = fullname.upper()
                #     getacc.save()
                #     #update transaction table
                #     tbltransaction.objects.filter(acccode = admissionnoold).update(acccode = admissionno,accname = fullname.upper())
                # else:
                #     used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                #     used.save()
                # #updating the liabilities
                # if tblaccount.objects.filter(acccode = 'L'+str(admissionno)):
                #     getacc = tblaccount.objects.get(acccode = 'L'+str(admissionno))
                #     #getacc.acccode = 'L'+str(admissionno)
                #     getacc.accname = fullname.upper()
                #     getacc.save()
                #     #update transaction table
                #     tbltransaction.objects.filter(acccode = 'L'+str(admissionnoold)).update(acccode = 'L'+str(admissionno),accname = fullname.upper())
                # else:
                #     used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                #     #used.save()
                # #treating other liabilities
                # if tblaccount.objects.filter(acccode = 'C'+str(admissionno)):
                #     getacc = tblaccount.objects.get(acccode = 'C'+str(admissionno))
                #     #getacc.acccode = 'C'+str(admissionno)
                #     getacc.accname = fullname.upper()
                #     getacc.save()
                #     #update transaction table
                #     tbltransaction.objects.filter(acccode = 'C'+str(admissionnoold)).update(acccode = 'C'+str(admissionno),accname = fullname.upper())
                # else:
                #     used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                #    # used.save()




                return HttpResponseRedirect('/student/success/')
        else:
            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/edit_reg.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def studentreport(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.studentreport
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = klassreportform()
        school = get_object_or_404(School, pk=1)
        student =''
        if request.method == 'POST':
            form = studentreportform(request.POST, request.FILES)
            if form.is_valid():
                session= form.cleaned_data['session']
                klass= form.cleaned_data['klass']
                arm = form.cleaned_data['arm']
                dayboarding = form.cleaned_data['dayboarding']
                filtermethod = form.cleaned_data['filtermethod']
                disclass =''
                disarm = ''
                #excelfile
                if filtermethod == 'Class':
                   student = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admitted_arm','-sex')
                   disclass = klass
                elif filtermethod == 'Classroom':
                    student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = session,gone = False).order_by('fullname')
                    disclass = klass
                    disarm = arm
                elif filtermethod=='Day/Boarding':
                    student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = session,dayboarding = dayboarding,gone = False).order_by('-sex','fullname')
                    disclass = klass
                # for k in student:
                #   p1,p2=k.fathernumber.split(',')




                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=studentlist.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('studentlist')
                    ws.write(0, 4, school.name)
                    ws.write(1, 4, school.address)
                    ws.write(2, 2, '%s %s :: Student List for %s Session' %(disclass,disarm, session) )
                    ws.write(3, 0, 'Name')
                    ws.write(3, 1, 'Sex')
                    ws.write(3, 2, 'Admission No')
                    ws.write(3, 3, 'Class')
                    ws.write(3, 4, 'Arm')
                    ws.write(3, 5, 'House')
                    ws.write(3, 6, 'Day/Boarding')
                    ws.write(3, 7, 'Phone Number')
                    ws.write(3, 8, 'E-Mail')
                    k = 4
                    for jd in student:
                       ws.write(k, 0, jd.fullname)
                       ws.write(k, 1, jd.sex)
                       ws.write(k, 2, jd.admissionno)
                       ws.write(k, 3, jd.admitted_class)
                       ws.write(k, 4, jd.admitted_arm)
                       ws.write(k, 5, jd.house)
                       ws.write(k, 6, jd.dayboarding)
                       ws.write(k, 7, jd.fathernumber)
                       ws.write(k, 8, jd.fatheremail)
                       k += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('student/student_list.html', {
                      # 'p1':p1,'p2':p2,
                      'form': form,'school':school,'varuser':varuser,'students_list':student,'session':session,'disclass':disclass,'disarm':disarm}, RequestContext(request))
            else:
                 varerr = 'All Fields Are Required !'
                 return render_to_response('student/student_list.html', {'form': form,'school':school,'varerr':varerr}, RequestContext(request))
        else:
            form = klassreportform()
            return render_to_response('student/student_list.html', {'varuser':varuser,'form': form,'school':school}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def withdrawajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                # stateoforigin = LGA.objects.all().distinct('state').order_by('state')
                #for j in stateoforigin:
                #   print j
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = Student.objects.get(admitted_class = klass,admitted_arm = arm,admitted_session = currse,fullname = stuname,admissionno = admno)
                return render_to_response('student/regform1.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('student/regform1.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('student/regform1.html',{'gdata':gdata})


##**********WITHDRAW STUDENT BUTTON***************###########
def withdrawstudent(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.withdraw
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm
        searchform = StudentSearchForm()

        if request.method == 'POST':
            admissionnoold = request.POST['admissionnoold']
            reason = request.POST['reason']
            datewithdrawal = request.POST['datewithdrawal']
            if reason =='' or datewithdrawal =='':
                varerr = "It is required you state both the reason and date of withdrawal date"
                return render_to_response('student/withdraw.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
            stuinfo = Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
            submit = WithdrawnStudent(student = stuinfo.fullname,klass = stuinfo.admitted_class,arm = stuinfo.admitted_arm,admissionno = stuinfo.admissionno,reason = reason,date_withdrawn = datewithdrawal,userid = varuser,admitted_session = currse)
            stuinfo.gone = True
            stuinfo.save()
            submit.save()


        # import datetime
        #    today = datetime.datetime.now()
        #    tm = today.month
        #    if tm == 9 or tm == 10 or tm == 11 or tm == 12: #first term
        #        stuinfo.gone = True
        #        stuinfo.first_term = False
        #        stuinfo.second_term = False
        #        stuinfo.third_term = False
        #        term = 'First'
        #        stuinfo.save()
        #    if tm == 1 or tm == 2 or tm == 3 or tm == 4: #second term
        #        stuinfo.gone = True
        #        stuinfo.second_term = False
        #        stuinfo.third_term = False
        #        term = 'Second'
        #        stuinfo.save()
        #    if tm == 5 or tm == 6 or tm == 7 or tm == 8: #third term
        #        stuinfo.gone = True
        #        stuinfo.first_term = True
        #        stuinfo.second_term = True
        #        stuinfo.third_term = False
        #        term = 'Third'
        #        stuinfo.save()

        #     deletig academi records
        #    akademics = StudentAcademicRecord(student=stuinfo, klass= stuinfo.admitted_class,arm= stuinfo.admitted_arm, term=term, session=stuinfo.admitted_session)
        #    akademics.save()
        #    AffectiveSkill(academic_rec=akademics).save()
        #    PsychomotorSkill(academic_rec=akademics).save()
        #    co = StudentAcademicRecord.objects.get(student=akrec, term = term)

            #TREATING THE ACCOUNT


            return HttpResponseRedirect('/student/success/')

        else:
            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/withdraw.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def returngonestudent(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.returngonestudent
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm
        searchform = StudentSearchForm()

        if request.method == 'POST':
        #form = StudentRegistrationForm(request.POST, request.FILES)
        #if form.is_valid():
            admissiono = request.POST['admissiono']
            reason = request.POST['reason']
            datewithdrawal = request.POST['datewithdrawal']
            if reason =='' or datewithdrawal =='':
                varerr = "Reason for withdrawal/withdrawal date is required"
                return render_to_response('student/returngoneform.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
            stuinfo = Student.objects.get(admissionno = admissiono,admitted_session = currse)
            stuinfo.gone = False
            stuinfo.save()
            WithdrawnStudent.objects.get(admissionno = admissiono,admitted_session = currse).delete()
            return HttpResponseRedirect('/student/success/')

        else:

            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/returngoneform.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def getstuinfogone(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm = acccode.split('-')
                #print klass,arm

                kk = []
                data = WithdrawnStudent.objects.filter(klass = klass,arm = arm,admitted_session = currse).order_by('student')
                for p in data:
                    jn = p.student+':'+p.admissionno
                    kk.append(jn)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def returnajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                # stateoforigin = LGA.objects.all().distinct('state').order_by('state')
                #for j in stateoforigin:
                #   print j
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = WithdrawnStudent.objects.get(klass = klass,arm = arm,admitted_session = currse,student = stuname,admissionno = admno)
                return render_to_response('student/regform2.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('student/regform2.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('student/regform2.html',{'gdata':gdata})

def withdrawnreport(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.withdrawnreport
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = withdrawnreportform()
        school = get_object_or_404(School, pk=1)
        student =''
        if request.method == 'POST':
            form = withdrawnreportform(request.POST, request.FILES)
            if form.is_valid():
                withdrawsession= form.cleaned_data['withdrawsession']
                student_list = []
                jclass = Class.objects.all()
                for klass in jclass:
                    student = WithdrawnStudent.objects.filter(klass = klass,admitted_session = withdrawsession).order_by('admissionno')
                    stdic = {'klass':klass,'student':student}
                    student_list.append(stdic)
                #student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = currse,dayboarding = dayboarding).order_by('sex','fullname')
                #disclass = klass
                #for u in student_list:
                 #   print u['klass']
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=withdranw_list.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('withdrawn_list')
                    ws.write(0, 1, school.name)
                    ws.write(1, 1, school.address)
                    ws.write(2, 2, ' Student  Withdrawn List for %s Session' %withdrawsession )
                    ws.write(3, 0, 'Name')
                    ws.write(3, 1, 'Admission No')
                    ws.write(3, 2, 'Class')
                    ws.write(3, 3, 'Arm')
                    ws.write(3, 4, 'Reason for Withdrawal')
                    ws.write(3, 5, 'Date Withdrawn')
                    k = 4
                    for jk in student_list :
                        ff = jk['klass']
                        #print ff
                        ws.write(k, 0, '%s' %ff)
                        k +=1
                        for jd in jk['student']:
                            ws.write(k, 0, jd.student)
                            ws.write(k, 1, jd.admissionno)
                            ws.write(k, 2, jd.klass)
                            ws.write(k, 3, jd.arm)
                            ws.write(k, 4, jd.reason)
                            ws.write(k, 5, jd.date_withdrawn.strftime("%d-%m-%Y"))
                            k += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('student/withdrawn_report.html', {'form': form,'school':school,'students_list':student_list,'session':withdrawsession}, RequestContext(request))

        else:
            form = withdrawnreportform()

            return render_to_response('student/withdrawn_report.html', {'varuser':varuser,'form': form,'school':school}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def searchstudent(request,vid):
    if  "userid" in request.session:
      stuinfo = Student.objects.get(id = vid)
      return render_to_response('student/search.html',{'data':stuinfo})
    else:
        return HttpResponseRedirect('/login/')


def searchprofile(request):
    if  "userid" in request.session:
      user = request.session['userid']
      stuinfo = Student.objects.get(fullname = user,admitted_session=currse)
      return render_to_response('student/profile.html',{'data':stuinfo,'varuser':user})
    else:
        return HttpResponseRedirect('/login/')


def studentsuccessful(request):
    return render_to_response('student/success.html', {}, RequestContext(request))


def get_report(request, type='student'):
    '''gets a report on a given model defined by type. returns html, pdf or xls.
    type can be either student or withdrawn. if type is student the additional filter arg
    defines queryset filter to select. filter keys are klass, arm, dayboarding'''
    format = request.GET.get('format', 'html')
    school = get_object_or_404(School, pk=1)

    if type == 'student':
        filter = {'gone': False}

        if request.GET.get('class'):
            filter.update({'admitted_class': request.GET.get('class')})
        if request.GET.get('arm'):
            filter.update({'admitted_arm': request.GET.get('arm')})
        if request.GET.get('boarding'):
            filter.update({'dayboarding': True})

        queryset = Student.objects.filter(**filter)
        title = 'List of Students'
        template = 'student/student_list.html'

    elif type == 'withdrawn':
        queryset = Student.objects.filter(gone=True)
        title = 'List of Withdrawn Students'
        template = 'student/withdrawn_student_list.html'

    context = {'students_list': queryset, 'report_title': title, 'school': school}

    if format == 'html':
        return render_to_response(template, context)
    elif format == 'pdf':
        render_to_pdf(template, context)
    elif format == 'xls':
        render_to_xls(context)
    else: return Http404



# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request, gone=False):
    term = request.GET.get('term')

    qset = Student.objects.filter(fullname__icontains=term, gone=gone)[:15]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s %s %s' % (i.fullname, i.admitted_class, i.admitted_arm), 'value': i.pk})
    return suggestions

@json_view
def get_lga_as_list(request, state=None):
    lgas = LGA.objects.filter(state__iexact=state)
    lga_list = []

    for lga in lgas:
        lga_list.append(lga.lga)

    lga_list.sort()
    return lga_list

#************function for student search ****************
def studentsearchajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render_to_response("namesearch.html")
                else:
                  data = Student.objects.filter(admitted_session = currse,surname__contains = acccode)
                  return render_to_response('student/sear.htm',{'data':data,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def studentsearchajax1(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                data = Student.objects.filter(admitted_session = currse,admissionno__contains = acccode,gone = False)
                return render_to_response('student/sear.htm',{'data':data,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')








from platformowners.utils import *
from sysadmin.forms import *
from academics.models import *
from sysadmin.models import *
# from student.models import Student
from student.forms import *
from django.core.serializers.json import json
from django.contrib.sessions.models import Session


import datetime
from datetime import date,time,datetime


from utilities.views import *
from bill.models import *
from bill.utils import getrandom
from setup.models import *
from setup.models import *
from bisect import bisect_left
import os
from assessment.getordinal import *
from django.core.mail import send_mail
from settings import MEDIA_ROOT as m_root



import shutil
from shutil import copy2
import settings
import random



def index(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=tbluserprofile.objects.filter(email=email,password=password,status=1)
        if user.count() ==1:
            user=user.get()
            request.session['userid'] = user.email
            varuser = request.session['userid']
            return  HttpResponseRedirect('/welcome/')


        # else:
        #     cc = tblstudent.objects.filter(wallet=email,status=1,phone=password)
        #     if cc.count==1:
        #         cc=cc.get()
        #         request.session['userid'] = email
        #         varuser = request.session['userid']
        #         return  HttpResponseRedirect('/home/')



            
        varerr = "Invalid Login Credentials, Contact Administrator"
        return render_to_response('login.html',{'varerr':varerr})


        # try:
        #     user=Student.objects.get(admissionno=username.upper(),surname=password, gone=False,admitted_session=currse)
        #     if user.admissionno==username.upper():
        #        request.session['userid'] = user.fullname
        #        return HttpResponseRedirect('/welcome/')
        # except:
             
        #     varerr = "Invalid Login Credentials, Contact Administrator"
        #     return render_to_response('login.html',{'varerr':varerr})
        
     

    else:
        return render_to_response('login.html')


def welcomecode(request):

    if  "userid" in request.session:
        varuser = request.session['userid']
        user = ratifyuser(varuser)


        dashboard=[]        
        
        f={'user':user}
        dashboard.append(f)


        return render_to_response('dashboard.html',
            {'dashboard':dashboard})  

    else:
        return HttpResponseRedirect('/login/')





def creatuser(request):
    if  "userid" in request.session:
        email = request.session['userid']
        user = ratifyuser(email)
      


        if user['admin']:

            if request.method == 'POST':

                email = request.POST['email']
                surname = request.POST['surname']
                firstname = request.POST['firstname']
                othername = request.POST['othername']
                phone = request.POST['phone']
                photo = request.POST['photo']

                staff_code=generate_code()


                tday = datetime.date.today()

                sss = tblstaff.objects.filter(email=email,status=1) # if user is active anywhere

                if sss.count() == 0:
                    tblstaff(branch =user['branch'],email=email,surname= surname,
                    firstname= firstname, othername= othername,  phone=phone,
                    photo= photo, staff_code=staff_code, status= 1).save()


                staf = tblstaff.objects.get(email=email,status=1)

                uuu = tbluserprofile.objects.filter(email  = email, status =1)

                if uuu.count() == 0:
                    tbluserprofile(branch=user['branch'],platformownwer = 0,platformadmin = 0,
                     email = email, password = staff_code,staffrec= staf, status = 1).save()
                    return HttpResponseRedirect('/controllers/createuser')

            else:




                
                # return render_to_response('sysadmin/createuser.htm',{'dashboard':user})
       

                
                return render_to_response('sysadmin/createuser.htm',{
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']}) 

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def resetusermain(request):
    varerr =""
    if  "userid" in request.session:
        email = request.session['userid']
        user = ratifyuser(email)

        if user['admin']:

            if request.method == 'POST':

                form = resetuserform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    email = form.cleaned_data['email']#

                    varvali = tbluserprofile.objects.filter(branch = user['branch'], email= email, status =1)
                    if varvali.count() == 1:
                        varvali=varvali.get()                        
                        varvali.password = "myschool"
                        varvali.save()
                        return HttpResponseRedirect('/controllers/resetuser/')


                    else:
                        return HttpResponseRedirect('/login/')


                return HttpResponseRedirect('/controllers/resetuser/')


            else:


                form = resetuserform()
                    
            return render_to_response('sysadmin/resetuser.htm',{'dashboard':user,'form':form})

        else:
            return HttpResponseRedirect('/login/')


    else:
        return HttpResponseRedirect('/login/')




def classteachermain(request):
    varerr =""
    if  "userid" in request.session:
        email = request.session['userid']

        user = ratifyuser(email)

        if user['admin']:
            if request.method == 'POST':
                form = classteacher(request.POST) # A form bound to the POST data
                if form.is_valid():
                    teachername1 = form.cleaned_data['teachername']
                    klass = form.cleaned_data['klass']
                    arm = form.cleaned_data['arm']
                    teachername = str(teachername1).lower()
                    if ClassTeacher.objects.filter(teachername=teachername):
                        varerr ="Class Already Taken By Teacher !"
                        getdetails = ClassTeacher.objects.filter(session = currse,co_ordinator='N/A').order_by('klass','arm')
                        return render_to_response('sysadmin/teacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    if teachername == "":
                        varerr ="Invalid User Name"
                        getdetails = ClassTeacher.objects.filter(session = currse).order_by('klass','arm')
                        return render_to_response('sysadmin/teacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    if ClassTeacher.objects.filter(klass = klass,arm = arm,session = currse, co_ordinator='N/A'):
                        varerr ="Class Already Taken By Teacher !"
                        getdetails = ClassTeacher.objects.filter(session = currse,co_ordinator='N/A').order_by('klass','arm')
                        return render_to_response('sysadmin/teacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    getsave = ClassTeacher(teachername = teachername,
                        klass = klass,
                        arm = arm,
                        co_ordinator='N/A',
                        userid = varuser,
                        session = currse)
                    getsave.save()
                    return HttpResponseRedirect('/controllers/classteacher/')

            else:
                form = classteacherform()
                getdetails = ClassTeacher.objects.filter(session = currse, co_ordinator='N/A').order_by('klass','arm')
            return render_to_response('sysadmin/teacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            return HttpResponseRedirect('/login/') 


    else:
        return HttpResponseRedirect('/login/') 



def header(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        vtoday = datetime.date.today()
        useracc = tbluserprofile.objects.get(email = email)
        schinfo = School.objects.get(id = 1)
        return render_to_response('header.html',{'schinfo':schinfo,'useracc':useracc,'vvtoday':vtoday.strftime("%B %d,%Y")})
    else:
        return HttpResponseRedirect('/login/')

        

def backup(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        if request.method == 'POST':
            source = "C:/windows/www/schapp/sofis.db" #os.path.normpath(os.path.dirname(sofis.db))
            dest = "C:/Users/o'mato/Desktop/backup.db"
            shutil.copy2(source, dest)
            return render_to_response('sysadmin/success1.html')
        else:
            return render_to_response('sysadmin/backupdb.htm')
    else:
        return HttpResponseRedirect('/login/')

def setdl(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        return render_to_response('sysadmin/deadlines.html',{'varuser':varuser})

    else:
        return HttpResponseRedirect('/login/')

def setr(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        return render_to_response('sysadmin/deadlines.html',{'varuser':varuser})

    else:
        return HttpResponseRedirect('/login/')


def cfsetdl(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        varerr=''
        transdate=''
        getdetails= tblcf.objects.all().order_by('deadline').reverse()
        access= 'Course Form'
        commence= 'deadline'
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        if request.method=='POST':
            form = cfform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                dl=form.cleaned_data['date']
                caldate2 = dl.split('/')
                transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                if tblcf.objects.filter(session=session,term=term).count()<1:
                    tblcf(session=session,term=term,deadline=transdate).save()
                else:
                    details= tblcf.objects.filter(session=session,term=term).update(deadline=transdate)
            else:
                varerr='Input date'

        else:
            form = cfform()
        return render_to_response('sysadmin/setdeadline.html',{'form':form,'commence':commence,'varerr':varerr, 'varuser':varuser,'getdetails':getdetails,'access':access})

    else:
        return HttpResponseRedirect('/login/')

def rsetr(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        varerr=''
        transdate=''
        access='Results'
        commence= 'Commencement'
        getdetails= tblresult.objects.all().order_by('deadline').reverse()
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        if request.method=='POST':
            form = rsform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                reportsheet=form.cleaned_data['reportsheet']
                dl=form.cleaned_data['date']
                caldate2 = dl.split('/')
                caldate2= map(int,caldate2)

                if reportsheet != '---':

                    transdate = date(caldate2[2],caldate2[0],caldate2[1])
                    fff =tblresult.objects.filter(session=session,reportsheet=reportsheet,term=term)
                    fdf = fff.count()

                    if fdf < 1:


                        tblresult(session=session,term=term,reportsheet=reportsheet,deadline=transdate).save()
                    else:
                        details= tblresult.objects.filter(reportsheet=reportsheet,session=session,term=term).update(deadline=transdate)

                    form = rsform()

                else:
                    varerr='Select reportsheet'
                

            else:
                varerr='Input date'

        else:
            form = rsform()
        return render_to_response('sysadmin/setdeadline.html',{'form':form,'commence':commence,'varerr':varerr, 'varuser':varuser,'getdetails':getdetails,'access':access})


def autorun(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        varerr=''
        if request.method=='POST':
            form=autorunform(request.POST)
            ca=request.POST['ca']
            session=request.POST['session']
            term=request.POST['term']
            varclass=[]
            myclasses= Class.objects.all()

            if term=='First':
                student = Student.objects.filter(first_term=True,admitted_session = session,
                    gone = False)
            elif term == 'Second':
                student = Student.objects.filter(second_term=True,admitted_session = session,
                     gone = False)
            elif term == 'Third':
                student = Student.objects.filter(third_term=True,admitted_session = session,
                 gone = False)


            for c in myclasses:
                c=str(c.klass)
                varclass.append(c)   #classes list


            for kl in varclass:
                category=kl[:2]



                coms=tblcom.objects.filter(category=category)
                stu=Student.objects.filter(admitted_class=kl, admitted_session=session,gone=False)


                if ca=='1st CA':
                    for j in stu:
                        if StudentAcademicRecord.objects.filter(student=j,term=term).count()>0:
                            acade=StudentAcademicRecord.objects.get(student=j,term=term)
                            avr=acade.stu_ave1 * 5  #compare this value with mean range
                            mid=[]
                            for cat in coms:
                                fb= cat.krang.split('-')[0]
                                fb=int(fb)
                                mid.append(fb)
                            mida=sorted(mid)
                            pos=0
                            pos=min(mida, key=lambda x:abs(x-float(avr)))
                            varerr='DONE WITH ZERO ERRORS'
                            coma=tblcom.objects.filter(krang__startswith=pos,category=category)
                            idvar=[]
                            for h in coma:
                                idvar.append(h.id)
                            idvar=idvar
                            uid=0
                            uid = random.choice(idvar)
                            esther=tblcom.objects.get(id=uid)
                            StudentAcademicRecord.objects.filter(student=j,term=term).update(com1=esther.comment)
                elif ca=='2nd CA':
                    for j in stu:
                        if StudentAcademicRecord.objects.filter(student=j,term=term).count()>0:
                            acade=StudentAcademicRecord.objects.get(student=j,term=term)
                            avr=acade.stu_ave2 * 5  #compare this value with mean range
                            mid=[]
                            for cat in coms:
                                fb= cat.krang.split('-')[0]
                                fb=int(fb)
                                mid.append(fb)
                            mida=sorted(mid)
                            pos=0
                            pos=min(mida, key=lambda x:abs(x-float(avr)))
                            varerr='DONE WITH ZERO ERRORS'
                            coma=tblcom.objects.filter(krang__startswith=pos,category=category)
                            idvar=[]
                            for h in coma:
                                idvar.append(h.id)
                            idvar=idvar
                            uid=0
                            uid = random.choice(idvar)
                            esther=tblcom.objects.get(id=uid)
                            StudentAcademicRecord.objects.filter(student=j,term=term).update(com2=esther.comment)

                elif ca == 'Mid Term': #SCORE SHEET':
                    for j in stu:
                        if StudentAcademicRecord.objects.filter(student=j,term=term).count()>0:
                            acade=StudentAcademicRecord.objects.get(student=j,term=term)
                            avr=int(acade.stu_ave1) * 5
                            mid=[]
                            for cat in coms:
                                fb= cat.krang.split('-')[0]
                                fb=int(fb)
                                mid.append(fb)
                            mida=sorted(mid)
                            pos=0
                            pos=min(mida, key=lambda x:abs(x-float(avr)))
                            varerr='DONE WITH ZERO ERRORS'
                            coma=tblcom.objects.filter(krang__startswith=pos,category=category)
                            idvar=[]
                            for h in coma:
                                idvar.append(h.id)
                            idvar=idvar
                            uid=0
                            uid = random.choice(idvar)
                            esther=tblcom.objects.get(id=uid)
                            StudentAcademicRecord.objects.filter(student=j,term=term).update(com2=esther.comment)


                elif ca=='End Term': #SUMMARY SHEET':
                    for j in stu:
                        if StudentAcademicRecord.objects.filter(student=j,term=term).count()>0:
                            acade=StudentAcademicRecord.objects.get(student=j,term=term)
                            avr=acade.stu_ave2  #compare this value with mean range
                            mid=[]
                            for cat in coms:
                                fb= cat.krang.split('-')[0]
                                fb=int(fb)
                                mid.append(fb)
                            mida=sorted(mid)
                            pos=0
                            pos=min(mida, key=lambda x:abs(x-float(avr)))
                            varerr='DONE WITH ZERO ERRORS'
                            coma=tblcom.objects.filter(krang__startswith=pos,category=category)
                            idvar=[]
                            for h in coma:
                                idvar.append(h.id)
                            idvar=idvar
                            uid=0
                            uid = random.choice(idvar)
                            esther=tblcom.objects.get(id=uid)

                            if term == 'Third':

                        #*************************#annual average********************
                                acaderec = StudentAcademicRecord.objects.get(student = j,term = term,session=session)
                                subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term,session = session).order_by('num')
                                totalmark24 = 0
                                rtotal4 = 0
                                totalmark4 =subsco.aggregate(Sum('annual_avg'))
                                totalmark24 = totalmark4['annual_avg__sum']
                                rtotal4 = float(totalmark24)



                                stave=subsco.count()
                                stave=rtotal4 / stave


                                if category == 'SS':
                                    st_grade = studentaveragedrader(float(stave))  #grading student average
                                elif category=='JS':
                                    st_grade = juniorgrade(float(stave))


                                student_grade=st_grade['grade']

                                kklass = j.admitted_class

                                caat=kklass[:2]

                                fig = kklass[3]

                                if caat== 'JS':
                                    if fig == '1':
                                        nxt = caat + " " + '2'
                                    elif fig == '2':
                                        nxt = caat + " " + '3'
                                    elif caat == '3':
                                        nxt= 'SS 1'

                                if caat== 'SS':
                                    if fig == '1':
                                        nxt = caat + " " + '2'
                                    elif fig == '2':
                                        nxt = caat + " " + '3'
                                    elif caat == '3':
                                        nxt= ''

                                if fig == '3':
                                    pass

                                else:
                                    if student_grade=='F':
                                        comment = esther.comment + ' Advice to repeat'
                                    else:
                                        comment=esther.comment + ' Promoted to ' + nxt

                                    # msg=nxt
                                    # return render_to_response('assessment/selectloan.html',{'msg':msg})

                                StudentAcademicRecord.objects.filter(student=j,term=term).update(principal_comment=comment)


                            else:
                                StudentAcademicRecord.objects.filter(student=j,term=term).update(principal_comment=esther.comment)

                else:
                    varerr="i ain't ready "
                    avr =0

            return render_to_response('sysadmin/autorun.html',{'form':form,'catu':varerr, 'varerr':varerr,'session':session,'assessment':ca,})
        else:
            form=autorunform()
        return render_to_response('sysadmin/autorun.html',{'form':form,'session':currse})
    else:
        return HttpResponseRedirect('/login/')

def userviews(request):
    if 'userid' in request.session:
        if request.is_ajax():
            if request.method=='POST':                        
                varuser=request.session['userid']
                post = request.POST.copy()
                acccode = post['userid']
                myviews=tbluserprofile.objects.filter(status='ACTIVE',username=varuser)
                return render_to_response('welcome.html',{'myviews':myviews})
    else:
        return HttpResponseRedirect('/login/')

def comauto(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=tbluserprofile.objects.get(username=varuser)
        uenter=user.createuser
        varerr=''
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        autocom = tblcom.objects.all().order_by('category','krang')
        if request.method=='POST':
            form = autocomform(request.POST)
            if form.is_valid():
                category=form.cleaned_data['category']
                rang=form.cleaned_data['krang']
                comment=form.cleaned_data['comment']
                comment = str(comment).lower()
                com=tblcom.objects.filter(category=category)#allfilter(category=category)
                if tblcom.objects.filter(category=category).count()==0:
                    com=tblcom(comment=comment,category=category,krang=rang).save()
                else:
                    r=0
                    for j in com:
                        if j.comment==comment:
                            varerr='COMMENT ALREADY EXIST'
                            return render_to_response('sysadmin/auto.html',{'form':form,'varerr':varerr, 'autocom':autocom})
                        else:
                            r=1
                    if r==1:
                        com=tblcom(comment=comment,category=category,krang=rang).save()
            else:
                varerr='you forgot to enter comment'
                form=autocomform(request.POST)
        else:
            varerr=''
            form=autocomform()
        form=autocomform()
        return render_to_response('sysadmin/auto.html',{'form':form,'varerr':varerr, 'autocom':autocom})
    else:
        return render_to_response('/login/')

def codi(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form = cocoform(request.POST) # A form bound to the POST data
            if form.is_valid():
                teachername1 = form.cleaned_data['teachername']
                klass = form.cleaned_data['klass']
                teachername = str(teachername1).lower()
                if ClassTeacher.objects.filter(klass = klass,session = currse,teachername = 'N/A'):
                    varerr ="Class Already Taken By Teacher !"
                    getdetails = ClassTeacher.objects.filter(session = currse,teachername = 'N/A').order_by('klass')
                    return render_to_response('sysadmin/codi.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                getsave = ClassTeacher(teachername = 'N/A',
                    klass = klass,
                    co_ordinator=teachername,
                    arm = 'N/A',
                    userid = varuser,
                    session = currse)
                getsave.save()
                return HttpResponseRedirect('/controllers/coco/')
        else:
            form = cocoform()
            getdetails = ClassTeacher.objects.filter(session = currse, teachername = 'N/A').order_by('klass')
        return render_to_response('sysadmin/codi.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

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



def subject_report(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False:
            return HttpResponseRedirect ('/sysadmin/access-denied/')
        varerr= ''
        getdetails = ''
        if request.method == 'POST':
            form = subject_report_form(request.POST)
            if form.is_valid():
                term = request.POST['term']
                subject = request.POST['subject']
                session = request.POST['session']
                klass = request.POST['klass']
                subclass = request.POST['subclass']
                stlist = SubjectScore.objects.filter(term = term, subject = subject, session = session, klass=klass).order_by('end_term_score').reverse()
                return render_to_response('sysadmin/subject-report.htm',{'subject':subject, 'klass':klass,'session':session,'varerr':varerr,'form':form,'getdetails':stlist},context_instance = RequestContext(request))
            else:
                stlist=[]
                varerr = 'FORM NOT VALID'
                form = subject_report_form()
                return render_to_response('sysadmin/subject-report.htm', {'form': form,'getdetails':stlist,'varerr':varerr},context_instance = RequestContext(request))
        else:
            stlist=[]
            form = subject_report_form()
            varerr = ''
            getdetails = '' #SubjectScore.objects.filter(session = session, term = term, klass = nclass, subject = subject).order_by('end_term_score')
        return render_to_response('sysadmin/subject-report.htm', {'form': form,'getdetails':stlist,'varerr':varerr},context_instance = RequestContext(request))
    else:
        form = form = subject_report_form(request.POST)
        varerr =""
        return render_to_response('login.html')


def subject_reports(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False:
            return HttpResponseRedirect ('/sysadmin/access-denied/')
        varerr= ''
        getdetails = ''
        if request.method == 'POST':
            form = subject_report_form(request.POST)
            if form.is_valid():
                #session = request.POST['session']
                term = request.POST['term']
                subject = request.POST['subject']
                session = request.POST['session']
                klass = request.POST['klass']
                subclass = request.POST['subclass']
                stlist=[]
                for j in Student.objects.filter(admitted_session=session, admitted_class = klass, gone = False):
                    if StudentAcademicRecord.objects.filter(student=j, session=session, term=term):
                        st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                        if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,term =term).order_by('end_term_score').reverse:
                            gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,term =term)
                            kk = {'house':gs.academic_rec.student.house,'admissionno':j.admissionno,'fullname':j.fullname,'klass':gs.klass,'arm':gs.arm,'sex':j.sex,'subject':gs.subject,'term':term,'end_term_score':gs.end_term_score}
                            stlist.append(kk)
                            stlist.sort()
                           # stlist.reverse()
                           # getdetails = SubjectScore.objects.filter(session = session, term = term, klass = klass, subject = subject).order_by('end_term_score').reverse
                return render_to_response('sysadmin/subject-report.htm',{'varerr':varerr,'form':form,'getdetails':stlist})
            else:
                stlist=[]
                varerr = 'PLEASE ENTER SESSION'
                form = subject_report_form()
                return render_to_response('sysadmin/subject-report.htm', {'form': form,'getdetails':stlist,'varerr':varerr},context_instance = RequestContext(request))
        else:
            stlist=[]
            form = subject_report_form()
            varerr = ''
            getdetails = '' #SubjectScore.objects.filter(session = session, term = term, klass = nclass, subject = subject).order_by('end_term_score')
        return render_to_response('sysadmin/subject-report.htm', {'form': form,'getdetails':stlist,'varerr':varerr},context_instance = RequestContext(request))
    else:
        form = form = subject_report_form(request.POST)
        varerr =""
        return render_to_response('login.html')


def subrepajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                accode = post['userid']
                state = accode
                kk = []
                if Subject.objects.filter(category = state):
                    data= Subject.objects.filter(category = state).order_by('num')
                    for j in data:
                        kk.append(j.subject)
                else:
                    kk.append('NIL')
                return HttpResponse(json.dumps(kk), mimetype ='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')





def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')

def changepassword(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        if request.method == 'POST':
            form = changepassform(request.POST) # A form bound to the POST data
            if form.is_valid():
                oldpassword = form.cleaned_data['oldpassword']
                password = form.cleaned_data['password']
                password2 = form.cleaned_data['password2']
                if password == password2:
                    try:
                        user = tbluserprofile.objects.get(username = varuser,password=oldpassword)
                        #user = tbluseracc.objects.get(username = varuser)
                        user.password = password.lower()
                        user.save()
                        #********************************************
                        from ruffwal.rwadmin.models import tbluseracc
                        user = tbluseracc.objects.get(username = varuser,password=oldpassword)
                        user.password = password.lower()
                        user.save()
                        from hrm.rcwadmin.models import tbluseracc as rcad
                        user2 = rcad.objects.get(username = varuser,password=oldpassword)
                        user2.password = password.lower()
                        user2.save()
                        return HttpResponseRedirect('/logout/')
                    except:
                        varerr = "Invalid User"
                        return HttpResponseRedirect('/welcome/')
                else:
                    return HttpResponseRedirect('/welcome/')
            else:
                return HttpResponseRedirect('/welcome/')
        else:
            return HttpResponseRedirect('/welcome/')

    else:
        return HttpResponseRedirect('/login/')

def unatho(request):
    return render_to_response('unautorise.htm',{})

def getchangepassword(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                useracc = tbluserprofile.objects.get(email = email)
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #getdetails =  tbltemp.objects.get(id = acccode)
                form = changepassform()
                return render_to_response('changepass.htm',{'varuser':varuser,'varerr':varerr,'form':form,'user':useracc.username,'pass':useracc.password})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def change_password(request):
    if  "userid" in request.session:
            # form = changepassform()    
            varuser = request.session['userid']
            useracc = tbluserprofile.objects.get(email = email)
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                #getdetails =  tbltemp.objects.get(id = acccode)
                form = changepassform()
                return render_to_response('changepass.htm',{'varuser':varuser,'form':form,'user':useracc.username})
            else:
                return render_to_response('changepass.htm',{'varuser':varuser,'user':useracc.username,'pass':useracc.password})
    else:
        return HttpResponseRedirect('/login/')

# def newuser(request):
#     if  "userid" in request.session:
#         varuser = request.session['userid']
#         user = tbluserprofile.objects.get(email = email)
#         uenter = user.createuser
#         if uenter is False :
#             return HttpResponseRedirect('/welcome/')
#         varerr = ""
#         getdetails =''
#         # if request.method == 'POST':
#         #     form = creatuserform(request.POST) # A form bound to the POST data
#         #     if form.is_valid():
#         username = request.post['username']
#         staffname = request.POST['staffname']
#                 tday = date.today()
#                 if tbluserprofile.objects.filter(username = username):
#                     varerr = "User In Existence !"
#                     getdetails = tbluserprofile.objects.all().order_by('staffname')
#                     return render_to_response('sysadmin/createuser.htm',{'varerr':varerr,'form':form,'getdetails':getdetails})
#                 user = tbluserprofile(username = username.lower(),password='myschool',staffname =  staffname.lower(),expires = tday,status ='ACTIVE',userid = varuser,created = date.today())
#                 user.save()
#                 try:
#                        #********************************************
#                         from ruffwal.rwadmin.models import tbluseracc
#                         user = tbluseracc(username = username.lower(),password='myschool',staffname =  staffname.lower(),expiredate = tday,status ='ACTIVE',userid = varuser)
#                         user.save()
#                         from hrm.rcwadmin.models import tbluseracc as rcad
#                         user2 = rcad(username = username.lower(),password='myschool',staffname =  staffname.lower(),expiredate = tday,status ='ACTIVE',userid = varuser)
#                         user2.save()
#                         return HttpResponseRedirect('/controllers/createuser')
#                 except:
#                         varerr = "This User Can Not be Created"
#                         return HttpResponseRedirect('/controllers/createuser')
#         else:
#             form = creatuserform()
#             getdetails = tbluserprofile.objects.filter(status='ACTIVE').order_by('staffname')
#         return render_to_response('sysadmin/createuser.htm',{'varerr':varerr,'form':form,'getdetails':getdetails})
#     else:
#         return HttpResponseRedirect('/login/')



def creatuserp(request):
    k = ['SS 1', 'SS 2', 'SS 3']
    for k in k:
        rec = StudentAcademicRecord.objects.filter(klass=k,session='2021/2022',term ='First')
        for rec in rec:
            ag_sc=SubjectScore.objects.filter(subject='AGRICULTURAL SCIENCE', academic_rec=rec,term='First',session='2021/2022').delete()





        

def usersearchajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render_to_response("namesearch.html")
                else:
                  data = tbluserprofile.objects.filter(status = 'ACTIVE', staffname__contains = acccode)
                  return render_to_response('sysadmin/user_ajax.html',{'getdetails':data,'session':acccode})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def usersearchajax1(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render_to_response("namesearch.html")
                else:
                  data = tbluserprofile.objects.filter(status = acccode)
                  return render_to_response('sysadmin/user_ajax.html',{'getdetails':data,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def dashboard(request):
    if "userid" in request.session:
        return render_to_response('dashboard.html')
    else:
        HttpResponseRedirect('/login/')
def getuseraccountmain(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbluserprofile.objects.get(id = acccode)
                return render_to_response('sysadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editusermain(request,ind):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
           return HttpResponseRedirect('/welcome/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            username = request.POST["username"]
            staffname = request.POST["staffname"]
            status = request.POST["status"]
            uname = str(staffname)
            uname = uname.lower()
            uuname = uname.replace(' ','-')
            #********************************************
            #****************************************************
            getdetails = tbluserprofile.objects.get(id = ind)
            getdetails.staffname = uuname
            getdetails.status = status
            getdetails.userid = varuser
            getdetails.save()
            try:

                from ruffwal.rwadmin.models import tbluseracc
                getdetails = tbluseracc.objects.get(id = ind)
                getdetails.staffname = uuname
                getdetails.status = status
                getdetails.userid = varuser
                getdetails.save()

                from hrm.rcwadmin.models import tbluseracc as rcad
                getdetails = rcad.objects.get(id = ind)
                getdetails.staffname = uuname
                getdetails.status = status
                getdetails.userid = varuser
                getdetails.save()

                return HttpResponseRedirect('/controllers/createuser/')

            except:
                return HttpResponseRedirect('/controllers/createuser/')
        else:
            return HttpResponseRedirect('/controllers/createuser/')

        #return render_to_response('sysadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')


def getstudentacademic(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbluserprofile.objects.get(id = acccode)
                if getdetails.setup is True:
                    setup = 'checked'
                else:
                    setup = 'unchecked'

                if getdetails.studentregistration is True:
                    studentregistration = 'checked'
                else:
                    studentregistration = 'unchecked'

                if getdetails.editregistration is True:
                    editregistration = 'checked'
                else:
                    editregistration = 'unchecked'

                if getdetails.studentreport is True:
                    studentreport = 'checked'
                else:
                    studentreport = 'unchecked'

                if getdetails.withdraw is True:
                    withdraw = 'checked'
                else:
                    withdraw = 'unchecked'

                if getdetails.returngonestudent is True:
                    returngonestudent = 'checked'
                else:
                    returngonestudent = 'unchecked'

                if getdetails.withdrawnreport is True:
                    withdrawnreport = 'checked'
                else:
                    withdrawnreport = 'unchecked'

                if getdetails.expensedecription is True:
                    expensedecription = 'checked'
                else:
                    expensedecription = 'unchecked'

                if getdetails.billsetup is True:
                    billsetup = 'checked'
                else:
                    billsetup = 'unchecked'

                if getdetails.additionalexpenses is True:
                    additionalexpenses = 'checked'
                else:
                    additionalexpenses = 'unchecked'

                if getdetails.printbill is True:
                    printbill = 'checked'
                else:
                    printbill = 'unchecked'

                if getdetails.billschedule is True:
                    billschedule = 'checked'
                else:
                    billschedule = 'unchecked'

                if getdetails.reportsheet is True:
                    reportsheet = 'checked'
                else:
                    reportsheet = 'unchecked'

                if getdetails.broadsheet is True:
                    broadsheet = 'checked'
                else:
                    broadsheet = 'unchecked'
                return render_to_response('sysadmin/edituseraca.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'setup':setup,'studentregistration':studentregistration,'editregistration':editregistration,'studentreport':studentreport,'withdraw':withdraw,'returngonestudent':returngonestudent,'withdrawnreport':withdrawnreport,'expensedecription':expensedecription,'billsetup':billsetup,'additionalexpenses':additionalexpenses,'printbill':printbill,'billschedule':billschedule,'reportsheet':reportsheet,'broadsheet':broadsheet},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')





def edituseraca(request,ind):
    setup = False
    studentregistration = False
    editregistration=  False
    studentreport = False
    withdraw = False
    returngonestudent = False
    withdrawnreport = False
    expensedecription = False
    billsetup = False
    additionalexpenses = False
    printbill = False
    billschedule = False
    reportsheet = False
    broadsheet = False
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
          return HttpResponseRedirect('/welcome/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            #********************************************
            #****************************************************
            if "setup" in request.POST:
                setup = True
            if "studentregistration" in request.POST:
                studentregistration = True
            if "editregistration" in request.POST:
                editregistration = True
            if "studentreport" in request.POST:
                studentreport = True
            #***************************************************
            if "withdraw" in request.POST:
                withdraw = True
            if "returngonestudent" in request.POST:
                returngonestudent = True
            if "withdrawnreport" in request.POST:
                withdrawnreport = True
            if "expensedecription" in request.POST:
                expensedecription = True
            if "billsetup" in request.POST:
                billsetup = True
                #************************
            if "additionalexpenses" in request.POST:
                additionalexpenses = True
            if "printbill" in request.POST:
                printbill = True
            if "billschedule" in request.POST:
                billschedule = True
            if "reportsheet" in request.POST:
                reportsheet = True
            if "broadsheet" in request.POST:
                broadsheet = True
            try:
                getdetails = tbluserprofile.objects.get(id = ind)
                getdetails.setup = setup
                getdetails.studentregistration = studentregistration
                getdetails.editregistration = editregistration
                getdetails.studentreport = studentreport
                getdetails.withdraw = withdraw
                getdetails.returngonestudent = returngonestudent
                getdetails.withdrawnreport = withdrawnreport
                getdetails.expensedecription = expensedecription
                getdetails.billsetup =  billsetup
                getdetails.additionalexpenses = additionalexpenses
                getdetails.printbill = printbill
                getdetails.billschedule = billschedule
                getdetails.reportsheet =  reportsheet
                getdetails.broadsheet = broadsheet
                getdetails.userid = varuser
                getdetails.save()
                return HttpResponseRedirect('/controllers/createuser/')

            except:
                return HttpResponseRedirect('/controllers/createuser/')

                #*****************************
        else:

            return HttpResponseRedirect('/controllers/createuser/')
    else:
        return HttpResponseRedirect('/login/')


def getadmin(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbluserprofile.objects.get(id = acccode)
                if getdetails.createuser is True:
                    createuser = 'checked'
                else:
                    createuser = 'unchecked'
                return render_to_response('sysadmin/edituseradmin.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'createuser':createuser},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def homeview(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =tbluserprofile.objects.get(id = acccode, status='ACTIVE')
                if getdetails.configuration is True:
                    configuration = 'checked'
                else:
                    configuration = 'unchecked'

                if getdetails.enrollment is True:
                    enrollment='checked'
                else:
                    enrollment = 'unchecked'

                if getdetails.reportsheet is True:
                    reportsheet = 'checked'
                else:
                    reportsheet = 'unchecked'

                if getdetails.curriculum is True:
                    curriculum = 'checked'
                else:
                    curriculum = 'unchecked'

                if getdetails.billing is True:
                    billing = 'checked'
                else:
                    billing = 'unchecked'

                if getdetails.accounts is True:
                    accounts = 'checked'
                else:
                    accounts = 'unchecked'

                if getdetails.staffaffairs is True:
                    staffaffairs = 'checked'
                else:
                    staffaffairs = 'unchecked'

                if getdetails.controllers is True:
                    controllers = 'checked'
                else:
                    controllers = 'unchecked'
                return render_to_response('sysadmin/edithome.html',{'configuration':configuration,
                    'varuser':varuser,
                    'varerr':varerr,
                    'enrollment':enrollment,
                    'reportsheet':reportsheet,
                    'curriculum':curriculum,
                    'billing':billing,
                    'accounts':accounts,
                    'staffaffairs':staffaffairs,
                    'controllers':controllers,
                    'getdetails':getdetails},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def editmyhome(request,ind):
    configuration = 0
    enrollment=  0
    reportsheet = 0
    curriculum = 0
    billing = 0
    staffaffairs = 0
    accounts = 0
    controllers = 0
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
          return HttpResponseRedirect('/welcome/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            #********************************************
            #****************************************************
            if "configuration" in request.POST:
                configuration = True
            if "enrollment" in request.POST:
                enrollment = True
            if "reportsheet" in request.POST:
                reportsheet = True
            #***************************************************
            if "curriculum" in request.POST:
                curriculum = True
            if "billing" in request.POST:
                billing = True
            if "accounts" in request.POST:
                accounts = True
            if "staffaffairs" in request.POST:
                staffaffairs = True

            if "controllers" in request.POST:
                controllers = True
                #************************
        
            getdetails = tbluserprofile.objects.get(id = ind)
            getdetails.configuration=configuration
            getdetails.enrollment=enrollment
            getdetails.reportsheet=reportsheet
            getdetails.curriculum=curriculum
            getdetails.billing=billing
            getdetails.accounts=accounts
            getdetails.staffaffairs=staffaffairs
            getdetails.controllers=controllers
            getdetails.save()
            return HttpResponseRedirect('/controllers/createuser/')

        else:

            return HttpResponseRedirect('/controllers/createuser/')
    else:
        return HttpResponseRedirect('/login/')


def edituseradmin(request,ind):
    createuser = False
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
           return HttpResponseRedirect('/welcome/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            #********************************************
            #****************************************************
            if "createuser" in request.POST:
                createuser = True
            try:
                getdetails = tbluserprofile.objects.get(id = ind)
                getdetails.createuser = createuser
                getdetails.userid = varuser
                getdetails.save()
                return HttpResponseRedirect('/controllers/createuser/')

            except:
                return HttpResponseRedirect('/controllers/createuser/')

                #*****************************
        else:

            return HttpResponseRedirect('/controllers/createuser/')
    else:
        return HttpResponseRedirect('/login/')


def adminunautomain(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('sysadmin/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')





       


def subjectgroupmain(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form = grpteacher(request.POST) # A form bound to the POST data
            if form.is_valid():
                teachername1 = form.cleaned_data['teachername']
                klass = form.cleaned_data['klass']
                grp = form.cleaned_data['grp']
                subject = form.cleaned_data['subject']
                teachername = str(teachername1).lower()
                if groupteacher.objects.filter(klass = klass,group=grp,session = currse,subject = subject,teachername = teachername):
                    varerr ="CANT'T ASSIGN USER TO TWO GROUPS OF SAME SUBJECT !"
                    getdetails = groupteacher.objects.filter(session = currse).order_by('klass','group')
                    return render_to_response('sysadmin/subjectgroup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                if groupteacher.objects.filter(klass = klass,session = currse,subject = subject,teachername = teachername):
                    varerr ="Subject Already Taken By Teacher !"
                    getdetails = groupteacher.objects.filter(session = currse).order_by('klass','group')
                    return render_to_response('sysadmin/subjectgroup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                

                if subjectteacher.objects.filter(teachername=varuser,klass=klass,subject=subject,session=currse).count()>0 :
                    varerr = 'set up not possible'
                    return HttpResponseRedirect('/controllers/subject_group/')
                else:                                    
                    getsave = groupteacher(teachername = teachername,klass = klass,group = grp,subject = subject,creator = varuser,session = currse,status = "ACTIVE")
                    getsave.save()
                return HttpResponseRedirect('/controllers/subject_group/')

            else:
                varerr ="Invalid User Name"
                getdetails = groupteacher.objects.filter(session = currse).order_by('klass','group')
                return render_to_response('sysadmin/subjectgroup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails})
        else:

            form = grpteacher()
            varerr='Enter username'
            getdetails = groupteacher.objects.filter(session = currse).order_by('klass','group')
        return render_to_response('sysadmin/subjectgroup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def getclassteacher(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = ClassTeacher.objects.get(id = acccode)
                return render_to_response('sysadmin/editclassteacher.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def daterr(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblterm.objects.get(id = acccode)
                form=dateform(request.POST)
                return render_to_response('sysadmin/deldate.html',{'form':form,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def duration(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblterm.objects.get(id = acccode)
                return render_to_response('sysadmin/dura.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getautocom(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblcom.objects.get(id = acccode)
                return render_to_response('sysadmin/esitcomment.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editautocomment(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            comment=request.POST['comment']
            tb=tblcom.objects.get(id=vid)
            cate=tb.category
            rang=tb.krang
            tb=tblcom.objects.filter(category=cate).order_by('category')
            r=0
            for j in tb:
                if j.comment==comment:
                    r=1
                    varerr='A similar Comment already exist for this category'        
                else:
                    r=0
            if r==0:
                co=tblcom.objects.filter(id=vid).update(comment=comment)
        return HttpResponseRedirect('/controllers/comauto/')

    else:
        return HttpResponseRedirect('/login/')

def ajaxrange(request):
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
                if gradingsys.objects.filter(classsub = state):
                  data1 = gradingsys.objects.filter(classsub = state).reverse()
                  for j in data1:
                      data.append(j.grade)
                return HttpResponse(json.dumps(data), mimetype='application/json')
                
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getcodi(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = ClassTeacher.objects.get(id = acccode)
                return render_to_response('sysadmin/editcodi.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
        


def deleteclassteacher(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = ClassTeacher.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/controllers/classteacher/')

    else:
        return HttpResponseRedirect('/login/')


def deletedate(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        if request.method=='POST':
            duration=request.POST['mydate']
            term = tblterm.objects.get(id = invid)
            term=term.term
            seldata = tblterm.objects.filter(id = invid).update(start_date=duration)


            stu = Student.objects.filter(admitted_session = currse,
                gone = False)

            for jkj in stu : 
                StudentAcademicRecord.objects.filter(student = jkj, session=currse,term=term).update(next_term_start=duration)
   

        return HttpResponseRedirect('/controllers/term-status/')

    else:
        return HttpResponseRedirect('/login/')



def deleteduration(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        if request.method=='POST':
            duration=request.POST['duration']
            term = tblterm.objects.get(id = invid)
            term=term.term
            seldata = tblterm.objects.filter(id = invid).update(duration=duration)
            StudentAcademicRecord.objects.filter(session=currse,term=term).update(days_open=duration)
   
        return HttpResponseRedirect('/controllers/term-status/')

    else:
        return HttpResponseRedirect('/login/')

def deletecoco(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = ClassTeacher.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/controllers/coco/')

    else:
        return HttpResponseRedirect('/login/')



def subjectteachermainf(request):
    varerr =""
    if  "userid" in request.session:
        term = ['First','Second', 'Third']
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form = sussss(request.POST) # A form bound to the POST data
            if form.is_valid():
                teachername1 = form.cleaned_data['teachername']
                klass = form.cleaned_data['klass']
                subject = form.cleaned_data['subject']
                rooms = form.cleaned_data['room']
                teachername = str(teachername1).lower()

                tttt= tbluserprofile.objects.filter(username=teachername)
                ttc=tttt.count()

                even_i=[]
                
                for i in range(0, len(rooms)):
                    if i % 2 ==0:
                        even_i.append(str(rooms[i]))

                # erw=[str(rooms[i]) for i in range (0,len(rooms)) if i % 2 == 0]

                if ttc == 1 :

                    try:

                        if groupteacher.objects.get(teachername=varuser, klass=klass,session=currse,subject=subject):
                            return HttpResponseRedirect('/controllers/subjectteacher/')
                    

                    except:
                        arm = rooms.upper()

                        # for kkk in even_i:
                        #     kkk=kkk.lower()
                        #     if kkk == 's':
                        #         arm='Science'
                        #     elif kkk == 'ar':
                        #         arm = 'Art'
                        #     elif kkk == 'co':
                        #         arm = 'Commercial'
                        #     else:
                        #         arm = kkk.upper()


                        for trm in term:
                            if subjectteacher.objects.filter(teachername=teachername, klass=klass,arm=arm,subject=subject,term=trm,session=currse).count()==0:

                                subjectteacher(teachername = teachername,klass = klass,arm = arm,
                                    subject = subject,term = trm,
                                    creator = varuser,session = currse,status = "ACTIVE").save()

                        
                        return HttpResponseRedirect('/controllers/subjectteacher/')


                    tbluserprofile.objects.filter(username=teachername).update(reportsheet=1)
                
                else:

                    return HttpResponseRedirect('/controllers/subjectteacher/')
        else:

            form = sussss()
            # varerr='wrong set up'
            getdetails = subjectteacher.objects.filter(session = currse).order_by('teachername','klass','arm','term')
        return render_to_response('sysadmin/subjectteacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')




def subjectteachermain(request):
    varerr =""
    if  "userid" in request.session:
        term = ['First','Second', 'Third']
  
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        getdetails =""
        
        if request.method == 'POST':
            form = suteacher(request.POST) # A form bound to the POST data
            if form.is_valid():
                teachername = form.cleaned_data['teachername']
                klass = form.cleaned_data['klass']
                arm = form.cleaned_data['arm']
                subject = form.cleaned_data['subject']

                # teachername = str(teachername1).lower()
                tttt= tbluserprofile.objects.filter(username=teachername)
                ttc=tttt.count()

                # return render_to_response('assessment/selectloan.html',{'msg':ttc})

                if ttc == 1 :

                    try:                    
                        if groupteacher.objects.get(teachername=varuser, 
                            klass=klass,
                            session=currse,
                            subject=subject):
                            return HttpResponseRedirect('/welcome/')

                    except:

                        for tm in term:
                            if subjectteacher.objects.filter(teachername=teachername, klass=klass,arm=arm, subject=subject,term=tm,session=currse).count()==0:
                                 subjectteacher(teachername = teachername,  klass = klass,arm = arm,  subject = subject,  term = tm,  creator = varuser, session = currse, status = "ACTIVE").save()
                                 tbluserprofile.objects.filter(username=teachername).update(reportsheet=1)

                        return HttpResponseRedirect('/controllers/subjectteacher/')

        else:

            form = suteacher()
            # varerr='wrong set up'
            getdetails = subjectteacher.objects.filter(session = currse).order_by('teachername','klass','arm','term')
        return render_to_response('sysadmin/subjectteacher.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')



# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term')
    gset = tbluserprofile.objects.filter(username__contains = term)[:10]
    suggestions = []
    for i in gset:
        suggestions.append({'label': '%s :: %s' % (i.username,i.staffname), 'username': i.username})
    return suggestions

@json_view
def autocompletes(request):
    term = request.GET.get('term')
    gset = tbluserprofile.objects.filter(username__contains = term)[:10]
    suggestions = []
    for i in gset:
        suggestions.append({'label': '%s :: %s' % (i.username,i.staffname), 'username': i.staffname})
    return suggestions


def getsubjectteacher(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = subjectteacher.objects.get(id = acccode)
                return render_to_response('sysadmin/editsubjectteacher.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getgrpteacher(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = groupteacher.objects.get(id = acccode)
                return render_to_response('sysadmin/editgrpteacher.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deletesubjectteacher(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = subjectteacher.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/controllers/subjectteacher/')

    else:
        return HttpResponseRedirect('/login/')

def deletegrpteacher(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = groupteacher.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/controllers/subject_group/')

    else:
        return HttpResponseRedirect('/login/')


def principalmain(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form = principalform(request.POST) # A form bound to the POST data
            if form.is_valid():
                teachername1 = form.cleaned_data['teachername']
                teachername = str(teachername1).lower()
                if teachername == "":
                    varerr ="Invalid User Name"
                    getdetails = Principal.objects.filter(session = currse).order_by('teachername')
                    return render_to_response('sysadmin/principal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                if Principal.objects.filter(session = currse,teachername = teachername):
                    varerr ="Teacher in Existence !"
                    getdetails = Principal.objects.filter(session = currse).order_by('teachername')
                    return render_to_response('sysadmin/principal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                getsave = Principal(teachername = teachername,userid = varuser,session = currse)
                getsave.save()
                return HttpResponseRedirect('/controllers/principal/')
        else:
            form = principalform()
            getdetails = Principal.objects.filter(session = currse).order_by('teachername')
        return render_to_response('sysadmin/principal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getprin(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = Principal.objects.get(id = acccode)
                return render_to_response('sysadmin/editprincipal.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deleteprincipal(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = Principal.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/controllers/principal/')

    else:
        return HttpResponseRedirect('/login/')

def expire(request,year):
    varerr =""
    vardate = datetime.date.today()
    vardate1 = vardate.strftime('%B %d,%Y')
    if request.method == 'POST':
        form = unlockform(request.POST) # A form bound to the POST data
        if form.is_valid():
            pin = form.cleaned_data['pin']
            if tblpin.objects.filter(ydate__year = year):
                gdate = tblpin.objects.get(ydate__year = year)
                gpin = gdate.pin
                k = encrypt(str(pin))
                if gpin == k:
                    l = encrypt1(str(pin))
                    gdate.used = l
                    gdate.save()
                    return HttpResponseRedirect('/login/')
                else:
                    varerr = "Invalid PIN"
                    return render_to_response('sysadmin/expire.htm',{'form':form,'varerr':varerr,'vardate1':vardate1,'year':year})
            else:
                varerr = "Invalid YEAR/PIN"
                return render_to_response('sysadmin/expire.htm',{'form':form,'varerr':varerr,'vardate1':vardate1,'year':year})

        else:
            varerr = "Invalid PIN"
            return render_to_response('sysadmin/expire.htm',{'form':form,'varerr':varerr,'vardate1':vardate1,'year':year})
    else:
        form = unlockform()
        return render_to_response('sysadmin/expire.htm',{'varerr':varerr,'vardate1':vardate,'form':form,'year':year})

def paybill(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = paybillform(request.POST) # A form bound to the POST data
            if form.is_valid():
                year = form.cleaned_data['year']
                tday = date(int(year),1,1)
                if tblpin.objects.filter(ydate__year = tday.year):
                    gdate = tblpin.objects.get(ydate__year = tday.year)
                    gpin = gdate.pin
                    gused = gdate.used
                    k = decrypt1(str(gused))
                    uu = encrypt(k)
                    if str(gpin) == str(uu):
                        varerr = "Year Already Paid For,Thank You"
                        return render_to_response('sysadmin/paybill.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        try:
                            del request.session['userid']
                        except KeyError:
                            pass
                        return HttpResponseRedirect('/controllers/page-expire/%s/'%int(tday.year))
                else:
                    try:
                        del request.session['userid']
                    except KeyError:
                        pass
                    return HttpResponseRedirect('/controllers/page-expire/%s/'%int(tday.year))
            else:
                varerr = "Invalid Year"
                return render_to_response('sysadmin/paybill.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = paybillform()
            return render_to_response('sysadmin/paybill.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


#Here We Enable And Disable Subject Term
def termenable(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')

        term1=['First','Third']
        term2=['Second','Third']
        term3=['First','Second']

        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form = teacherenableform(request.POST) # A form bound to the POST data
            if form.is_valid():
                term = form.cleaned_data['term']
                status = form.cleaned_data['status']
                if term == 'First':
                    if status =='ACTIVE':
                        tblterm.objects.filter(term=term).update(status=status)
                        for t in term2:
                            tblterm.objects.filter(term=t).update(status='INACTIVE')
                
                elif term == 'Second':
                    if status=='ACTIVE':
                        tblterm.objects.filter(term=term).update(status='ACTIVE')
                        for t in term1:
                            tblterm.objects.filter(term=t).update(status='INACTIVE')
                elif term=='Third':
                    if status=='ACTIVE':
                        tblterm.objects.filter(term=term).update(status='ACTIVE')
                        for t in term3:
                            tblterm.objects.filter(term=t).update(status='INACTIVE')
                sst = Student.objects.filter(admitted_session=currse)
                return HttpResponseRedirect('/controllers/term-status/')
        else:
            form = teacherenableform()
            getdetails = tblterm.objects.all()
        return render_to_response('sysadmin/enableterm.htm',
            {'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},
            context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')



def dataentry(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser        
        if uenter is False :
            return HttpResponseRedirect('/welcome/')

        getdetails = tblde.objects.get(id=1).status
        if getdetails==1:
            getdetails='checked'
            done='data entry is currently turned on'
        else:
            done='data entry is currently turned off'
            
        if request.method=='POST':
            if "dataentry" in request.POST:
                dataentry=True
                done='data entry turned on successfully'
            else:
                dataentry=False
                done='data entry turned off successfully'
            entry = tblde.objects.get(id=1)
            entry.status=dataentry
            entry.save()

 
        return render_to_response('sysadmin/dataentry.html',{'varuser':varuser,'checked':getdetails,'done':done})
    else:
        return HttpResponseRedirect('/login/')



def excemptions(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')

        getdetails = tblde.objects.all()
        return render_to_response('sysadmin/exempt.html',{'varuser':varuser,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def reportable(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')

        getdetails =""
        if request.method == 'POST':
            form = reportsheetform(request.POST) # A form bound to the POST data
            if form.is_valid():
                report = form.cleaned_data['report']
                status = form.cleaned_data['status']
                myreport=tblreportsheet.objects.get(reportsheet=report)
                myreport.status=status
                myreport.save()
                if myreport.reportsheet == 'Mid term':
                    if status == 'ACTIVE':
                        tblreportsheet.objects.filter(reportsheet='End term').update(status='INACTIVE')
                    else:
                        tblreportsheet.objects.filter(reportsheet='End term').update(status='ACTIVE')

                else:
                    if status == 'ACTIVE':
                        tblreportsheet.objects.filter(reportsheet='Mid term').update(status='INACTIVE')
                    else:
                        tblreportsheet.objects.filter(reportsheet='Mid term').update(status='ACTIVE')


                return HttpResponseRedirect('/controllers/reportsheet/')
        else:
            form = reportsheetform()
            getdetails = tblreportsheet.objects.all()
        return render_to_response('sysadmin/enablereport.html',{'varuser':varuser,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


#*****************************search for student *************************************
def search_student(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        return render_to_response('studentsearch.htm',{'varuser':varuser},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


#**************Promoting the student ****************************************
def student_promotion(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        succ =""
        if request.method == 'POST':
            succ =""
            form = promotion_form(request.POST)
            if form.is_valid():
                oldclass = request.POST['oldclass']
                newclass = request.POST['newclass']
                session = request.POST['session']
                subclass = request.POST['subclass']
                if oldclass > newclass:
                    succ ="Demotion not possible!!"
                    return render_to_response('sysadmin/promotion.htm',{'form': form,'succ':succ})
                
                if oldclass == newclass:
                    succ ="Current class Same as new class!!"
                    return render_to_response('sysadmin/promotion.htm',{'form': form,'succ':succ})
               
                if subclass == '---':
                    succ ="PLEASE SELECT APPRPRIATE SUBJECT CATEGORY"
                    return render_to_response('sysadmin/promotion.htm',{'form': form,'succ':succ})


                if Student.objects.filter(admitted_session = session, admitted_class = oldclass,gone = False).count()==0:
                    succ ="NO STUDENTS TO PROMOTE!!"
                    return render_to_response('sysadmin/promotion.htm',{'form': form,'succ':succ})
  
                x,y = str(session).split('/')
                k = int(x) + 1
                n = int(y) + 1
                newsession = str(k)+'/'+str(n)
  
                sj = Subject.objects.filter(category = subclass).count()
                sj = sj+1

                terrm = ['First', 'Second', 'Third']

                pk5 = Student.objects.filter(admitted_session = session, 
                    admitted_class = oldclass,
                    gone = False).order_by('admissionno')

                for p in pk5 :
                    ll = str(p.studentpicture).split('/')[1]
                    n,e = str(ll).split('.')
                    stpic = str(n)+'.'+str(e).lower()
                    sp = os.path.join(m_root, 'studentpix/%s'%stpic)

                    if os.path.exists(sp) is True:
                        pics = 'studentpix/'+stpic  #p.studentpicture
                    else:
                        pics = 'studentpix/user.png'


                    submit = Student(third_term = True,
                        second_term=True, 
                        first_term = True, 
                        birth_date= p.birth_date,
                        admitted_session = newsession,
                        firstname = p.firstname,
                        surname = p.surname,
                        othername = p.othername,
                        address = p.address,
                        sex = p.sex,
                        birth_place = p.birth_place,
                        state_of_origin =p.state_of_origin,
                        lga = p.lga,
                        fathername =p.fathername,
                        fatheraddress = p.fatheraddress,
                        fathernumber = p.fathernumber,
                        fatheroccupation =p.fatheroccupation,
                        fatheremail = p.fatheremail,
                        prev_school =p.prev_school,
                        prev_class = p.prev_class,
                        admitted_class = newclass,

                        admitted_arm = subclass.upper(),
                        subclass = subclass,

                        admissionno = p.admissionno,
                        house = p.house,
                        dayboarding = p.dayboarding,
                        
                        userid = p.userid,
                        studentpicture = p.studentpicture).save()


    ############# treating affective, psychomotive and subjectscore####################
                    

                    for term in terrm:
                        StudentAcademicRecord(student=p,
                            klass= newclass,
                            arm= subclass.upper(),
                            term=term,
                            session=newsession).save()

                        st = StudentAcademicRecord.objects.get(student=p,
                                term=term,
                                session=newsession)

                        AffectiveSkill(academic_rec=st).save()
                        PsychomotorSkill(academic_rec=st).save()


###############ADDING COMPUSORY SUBJECTS***************************************A
                        for n in range (1,sj):
                            sub = Subject.objects.get(category = subclass, num = n)

                            if sub.category2 == 'Compulsory':
                                tr =SubjectScore(academic_rec = st,
                                    subject = sub.subject, 
                                    num = n, klass = newclass, 
                                    session = newsession, 
                                    arm = subclass.upper(), 
                                    term = term).save()

#**********************88 treating accounts****************************
                succ = "Successful !!!"
                return render_to_response('sysadmin/promotion.htm',{'form': form,'succ':succ})
        else:
            form = promotion_form()
        return render_to_response('sysadmin/promotion.htm', {'form': form,'succ':succ})
    else:
        return HttpResponseRedirect('/login/')

#**************Updating The School Calendar ****************************************

def calendar_update(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        succ =""
        if request.method == 'POST':
            succ =""
            form = calendar_form(request.POST)
            if form.is_valid():
                oldsession = request.POST['session']
                sessionnew = request.POST['sessionnew']


                currentsession.objects.all().update(session =sessionnew)
                aalstu = Student.objects.filter(admitted_session=oldsession,gone=0)

                for kk in aalstu:

                    old_class = kk.admitted_class

                    if old_class =='JS 1':
                        newclass='JS 2'

                    elif old_class== 'JS 2':
                        newclass= 'JS 3'

                    elif old_class== 'SS 1':
                        newclass= 'SS 2'

                    elif old_class== 'SS 2':
                        newclass= 'SS 3'


                    subclass=kk.subclass
                    arm = kk.admitted_arm



                    if  old_class=='JS 3' or old_class=='SS 3':
                        sub=0

                    else:
                        try:
                            Student.objects.get(admissionno=kk.admissionno,
                                admitted_session=sessionnew)
                        except:

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
                                admitted_class = newclass,
                                admitted_arm = arm,
                                admissionno = kk.admissionno,
                                house = kk.house,
                                dayboarding = kk.dayboarding,
                                subclass = subclass,
                                userid = varuser,
                                # studentpicture = 'studentpix/user.png'
                                studentpicture = kk.studentpicture).save() #takenote



                newstu = Student.objects.filter(admitted_session=sessionnew,gone=0)

                for akrec in newstu:

                    terrm = ['First', 'Second', 'Third']
                    for term in terrm:

                        StudentAcademicRecord(student=akrec,
                            klass= akrec.admitted_class,
                            arm= akrec.admitted_arm,
                            term=term,
                            session=sessionnew).save()

                        co = StudentAcademicRecord.objects.get(student=akrec, term = term)

                        AffectiveSkill(academic_rec=co).save()
                        PsychomotorSkill(academic_rec=co).save()

                       #counts no of subjects
                        P = Subject.objects.filter(category = akrec.subclass).count()
                        P = P+1
                        for n in range (1,P):
                            sub = Subject.objects.get(category = akrec.subclass, num = n)
                            if sub.category2 == 'Compulsory':

                                SubjectScore(academic_rec = co,                                    
                                    subject = sub.subject, 
                                    num = n, 
                                    klass = akrec.admitted_class, 
                                    session = sessionnew, 
                                    arm = akrec.admitted_arm, 
                                    term = term).save()

            lk = tblterm.objects.filter().update(session=sessionnew,duration=0,start_date='2022-09-05')
            subjectteacher.objects.filter().update(session=sessionnew)
            ClassTeacher.objects.filter().update(session=sessionnew)
            tblresult.objects.all().delete()
            tblcf.objects.all().delete()
            Session.objects.all().delete()

            subjectteacher.objects.all().delete()
            ClassTeacher.objects.all().delete()

            # Migrationhistory.objects.all().delete()

            succ = "Successful !!!"
            return render_to_response('sysadmin/updatecalendar.htm',{'form': form,'succ':succ})
        else:
            form = calendar_form()
        return render_to_response('sysadmin/updatecalendar.htm', {'form': form,'succ':succ})
    else:
        return HttpResponseRedirect('/login/')


#for demo password *************************************************************
def passwordrequest(request):
    varerr = ""
    varerr2 = ""
    form = useraccform()
    vtoday = date.today()
    vvtoday = vtoday.year
    schinfo = School.objects.get(id = 1)
    if request.method == 'POST':
        form2 = userloginform(request.POST) # A form bound to the POST data
        if form2.is_valid():
            emailm = str(form2.cleaned_data['email']).lower()
            try:
                body ='Thank you for your interest in our school management software (SchApp) \n\n username : testuser \n\n password : 12345 \n\n\n Ruffwal Support Team \n +2348033204305,+2348062916005'
                body2 ="%s requested for user account for SchApp."%emailm
                send_mail('Demo Password For School Management Software',body, 'support@ruffwal.com',[emailm],fail_silently=False)
                send_mail('Demo Password For School Management Software',body2, 'support@ruffwal.com',['info@ruffwal.com'],fail_silently=False)
                varerr2 = "Check your email for your login details"
                return render_to_response('login.html',{'varerr2':varerr2,'form':form,'form2':form2,'schinfo':schinfo,'vvtoday':vvtoday},context_instance = RequestContext(request))
            except :
                varerr2 = "Error occurred, Please Check your connection"
                return render_to_response('login.html',{'varerr2':varerr2,'form':form,'form2':form2,'schinfo':schinfo,'vvtoday':vvtoday},context_instance = RequestContext(request))
        else:
            varerr2 = "Invalid E-mail !!!"
            return render_to_response('login.html',{'varerr2':varerr2,'form':form,'form2':form2,'schinfo':schinfo,'vvtoday':vvtoday},context_instance = RequestContext(request))
    else:
        form = useraccform()
        form2 = userloginform()
        return render_to_response('login.html',{'form':form,'form2':form2,'varerr':varerr,'schinfo':schinfo,'vvtoday':vvtoday})

#****************  Upload for the school website ***************************************
def online_result(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        succ =""
        if request.method == 'POST':
            succ =""
            form = online_result_form(request.POST)
            if form.is_valid():
                term = request.POST['term']
                newclass = request.POST['newclass']
                klass = newclass
                session = request.POST['session']
                if klass.startswith('J'):
                    k= Subject.objects.filter(category='JS').order_by('num')
                elif klass.startswith('Y'):
                     k= Subject.objects.filter(category='Year').order_by('num')
                else:
                   k= Subject.objects.all().exclude(category='Year').exclude(category='JS').order_by('num')
                subjdic = {}
                for sub in k:
                   jk = {sub.subject:sub.subject}
                   subjdic.update(jk)
                sublist = subjdic.keys()
                #print 'List of subjects',sublist
                stulist = []
                for p in Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False):
                    acaderec = StudentAcademicRecord.objects.get(student = p,session = session,term = term)
                    affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                    #*********treating subjects ********************************
                    getdic = {}
                    for js in sublist:
                        if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                           u = {js:{'ca1':0,'ca2':0,'exam':0,'termscore':0,'subavg':0,'grade':'Nil','remark':'Nil','teacher':'Nil'}}
                        else:
                           totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                           if term == "Third":
                              subavg = totsubject.annual_avg
                           else:
                               subavg = totsubject.end_term_score
                           u = {js:{'ca1':totsubject.first_ca,'ca2':totsubject.second_ca,'exam':totsubject.exam_score,'termscore':totsubject.end_term_score,'subavg':subavg,'grade':totsubject.grade,'remark':totsubject.remark,'teacher':totsubject.subject_teacher}}
                        getdic.update(u)

                    #*********************************************************
                    subject = SubjectScore.objects.filter(academic_rec = acaderec,term = term)
                    di = {'student':p,'academic':acaderec,'affective':affskill,'psyco':psycho,'subject':getdic}
                    stulist.append(di)
                response = HttpResponse(mimetype="application/ms-excel")
                titl = str(klass).replace(' ','') + '_'+str(term)
                response['Content-Disposition'] = 'attachment; filename=%s.xls'%titl
                wb = xlwt.Workbook()
                ws = wb.add_sheet('%s'%titl)
                v = 11
                ws.write(0,0,'Surname')
                ws.write(0,1,'Sex')
                ws.write(0,2,'Class')
                ws.write(0,3,'Session')
                ws.write(0,4,'Arm')
                ws.write(0,5,'Time School Open')
                ws.write(0,6,'Admission Number')
                ws.write(0,7,'No of Time Present')
                ws.write(0,8,'House')
                ws.write(0,9,'Next Term Begin')
                ws.write(0,10,'Term')
                for p in sublist:
                    ws.write(0, v, "ca1_"+str(p))
                    v += 1
                    ws.write(0, v, "ca2_"+str(p))
                    v += 1
                    ws.write(0, v, "exam_"+str(p))
                    v += 1
                    #ws.write(0, v, "end_term_score_"+str(p))
                    #v += 1
                    #ws.write(0, v, "subavg_"+str(p))
                    #v += 1
                    ws.write(0, v, "grade_"+str(p))
                    v += 1
                    ws.write(0, v, "remark_"+str(p))
                    v += 1
                    ws.write(0, v, "teacher_"+str(p))
                    v += 1
                ws.write(0, v, 'punctuality')
                v += 1
                ws.write(0, v, 'neatness')
                v += 1
                ws.write(0, v, 'honesty')
                v += 1
                ws.write(0, v, 'initiative')
                v += 1
                ws.write(0, v, 'self_control')
                v += 1
                ws.write(0, v, 'reliability')
                v += 1
                ws.write(0, v, 'perseverance')
                v += 1
                ws.write(0, v, 'politeness')
                v += 1
                ws.write(0, v, 'attentiveness')
                v += 1
                #ws.write(0, v, 'rel_with_people')
                #v += 1
                ws.write(0, v, 'cooperation')
                v += 1
                ws.write(0, v, 'organizational_ability')
                v += 1

                ws.write(0, v, 'handwriting')
                v += 1
                ws.write(0, v, 'games')
                v += 1
                ws.write(0, v, 'art')
                v += 1
                #ws.write(0, v, 'painting')
                #v += 1
                ws.write(0, v, 'music')
                v += 1
                ws.write(0, v, 'Class Teacher Remark')
                v += 1
                ws.write(0, v, 'Principal Remark')
                v += 1

                k = 1
                for jd in stulist:
                    c = 11
                    ws.write(k, 0, jd['student'].fullname)
                    ws.write(k, 1, jd['student'].sex)
                    ws.write(k, 2, jd['student'].admitted_class)
                    ws.write(k, 3, jd['student'].admitted_session)
                    ws.write(k, 4, jd['student'].admitted_arm)
                    ws.write(k, 5, jd['academic'].days_open)
                    ws.write(k, 6, jd['student'].admissionno)
                    ws.write(k, 7, jd['academic'].days_present)
                    ws.write(k, 8, jd['student'].house)
                    ws.write(k, 9, str(jd['academic'].next_term_start))
                    ws.write(k, 10, jd['academic'].term)
                    for q in sublist:
                        ws.write(k, c, jd['subject'][q]['ca1'])#.strftime("%d-%m-%Y")
                        c += 1
                        ws.write(k, c, jd['subject'][q]['ca2'])
                        c += 1
                        ws.write(k, c, jd['subject'][q]['exam'])
                        c += 1
                        #ws.write(k, c, jd['subject'][q]['termscore'])
                        #c += 1
                        #ws.write(k, c, jd['subject'][q]['subavg'])
                        #c += 1
                        ws.write(k, c, jd['subject'][q]['grade'])
                        c += 1
                        ws.write(k, c, jd['subject'][q]['remark'])
                        c += 1
                        ws.write(k, c, jd['subject'][q]['teacher'])
                        c += 1
                    ws.write(k, c, jd['affective'].punctuality)
                    c += 1
                    ws.write(k, c, jd['affective'].neatness)
                    c += 1
                    ws.write(k, c, jd['affective'].honesty)
                    c += 1
                    ws.write(k, c, jd['affective'].initiative)
                    c += 1
                    ws.write(k, c, jd['affective'].self_control)
                    c += 1
                    ws.write(k, c, jd['affective'].reliability)
                    c += 1
                    ws.write(k, c, jd['affective'].perseverance)
                    c += 1
                    ws.write(k, c, jd['affective'].politeness)
                    c += 1
                    ws.write(k, c, jd['affective'].attentiveness)
                    c += 1
                    #ws.write(k, c, jd['affective'].rel_with_people)
                    #c += 1
                    ws.write(k, c, jd['affective'].cooperation)
                    c += 1
                    ws.write(k, c, jd['affective'].organizational_ability)
                    c += 1

                    ws.write(k, c, jd['psyco'].handwriting)
                    c += 1
                    ws.write(k, c, jd['psyco'].games)
                    c += 1
                    ws.write(k, c, jd['psyco'].art)
                    c += 1
                    #ws.write(k, c, jd['psyco'].painting)
                    #c += 1
                    ws.write(k, c, jd['psyco'].music)
                    c += 1

                    ws.write(k, c, jd['academic'].class_teacher_comment)
                    c += 1
                    ws.write(k, c, jd['academic'].principal_comment)
                    c += 1

                    k += 1
                wb.save(response)
                return response
                succ = "Successful !!!"
                return render_to_response('sysadmin/onlineresult.htm',{'form': form,'succ':succ})
        else:
            form = online_result_form()
        return render_to_response('sysadmin/onlineresult.htm', {'form': form,'succ':succ})
    else:
        return HttpResponseRedirect('/login/')
#****************************Online Statement of account *************************
def online_statement(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = email)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/welcome/')
        varerr = ""
        succ =""
        if request.method == 'POST':
            succ =""
            form = statement_form(request.POST)
            if form.is_valid():
                session = request.POST['session']
                year = str(session).split('/')[1]
                varstart = date(int(year),1,1)
                varend = date(int(year),12,31)
                sublist = []
                for p in Student.objects.filter(admitted_session = session):
                    admno = p.admissionno
                    if tblaccount.objects.filter(acccode = admno):
                       acc = tblaccount.objects.get(acccode = admno)
                       accno = admno
                       getdata = tbltransaction.objects.filter(acccode = accno,transdate__range=(varstart,varend)).order_by('transdate','id')
                       bal = 0
                       dd ={}
                       getdetails =""
                       opbal = getopbal(accno,varstart,acc.groupname)
                       bal = opbal
                       ref = ""
                       dbal = ""
                       for jd in getdata:
                          groupname = jd.groupname
                          debit =jd.debit
                          credit = jd.credit
                          particulars = jd.particulars
                          refno =jd.refno
                          transdate = jd.transdate
                          accname =  jd.accname
                          acccode =  jd.acccode
                          transid = jd.transid
                          bal = bal + debit - credit
                          ref = ref +"tran date ="+ str(transdate.day)+"/"+str(transdate.month)+"/"+str(transdate.year)+"~"+"Particulars ="+str(particulars)+"~"+"references ="+str(refno)+"~"+"debit ="+str(debit)+"~"+"credit ="+str(credit)+"|"
                          dbal = dbal + str(bal)+"|"
                       j = {'name':str(p.surname).title() +' ' + str(p.firstname).title(),'accno':accno,'admno':admno,'lastdate':str(acc.lasttrandate.day)+"/"+str(acc.lasttrandate.month)+"/"+str(acc.lasttrandate.year),'openbal':opbal,'ref':ref,'balance':dbal}
                       sublist.append(j)
                    else:
                        pass
                response = HttpResponse(mimetype="application/ms-excel")
                titl = "statement"
                response['Content-Disposition'] = 'attachment; filename=%s.xls'%titl
                wb = xlwt.Workbook()
                ws = wb.add_sheet('%s'%titl)
                v = 1
                #ws.write(0,0,'Surname')
                ws.write(0,1,'Name')
                ws.write(0,2,'Account No')
                ws.write(0,3,'Admission No')
                ws.write(0,4,'Last Transaction Date')
                ws.write(0,5,'Opening Balance')
                ws.write(0,6,'transdate_particulars_references/chq/transfer_debit_credit')
                #ws.write(0,7,'Balance')
                for p in sublist:
                    ws.write(v, 1, p['name'])
                    ws.write(v, 2, p['accno'])
                    ws.write(v, 3, p['admno'])
                    ws.write(v, 4, p['lastdate'])
                    ws.write(v, 5, p['openbal'])
                    ws.write(v, 6, p['ref'])
                    #ws.write(v, 7, p['balance'])
                    v += 1
                wb.save(response)
                return response
                succ = "Successful !!!"
                return render_to_response('sysadmin/onlinestatement.htm',{'form': form,'succ':succ})
        else:
            form = statement_form()
        return render_to_response('sysadmin/onlinestatement.htm', {'form': form,'succ':succ})
    else:
        return HttpResponseRedirect('/login/')



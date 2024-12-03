# Create your views here.
from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from CBT.forms import *
from setup.models import *
from sysadmin.models import *
from student.models import *
from CBT.models import *
from CBT.utils import *
from django.core.serializers.json import json
import random
from django.db.models import Max,Sum
from academics.models import *
from utilities.views import *


from datetime import *

currse = currentsession.objects.get(id = 1)
term =tblterm.objects.get(status="ACTIVE")
term=term.term
school=School.objects.get(id =1)

dddy = datetime.today()
ttimee = dddy.time()

switch=0

    



def chroose(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        uuu=userprofile.objects.get(email=varuser)
        if uuu.createuser==1:
            return render_to_response('CBT/successad.html',{'varuser':varuser})
        else:
            return render_to_response('CBT/success.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def assignment(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        uza = userprofile.objects.get(email = varuser)
        uenter = uza.createuser
        if uenter is False :
            return HttpResponseRedirect('/cbt/access_denied/')

        if request.method=='POST':
            form= subform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                subject=form.cleaned_data['subject']
                user=form.cleaned_data['user']

                
                usercount=userprofile.objects.filter(email = user).count()
                if usercount == 0:
                    msg = 'INVALID USERNAME'
                    return render_to_response('CBT/entub.html',{'varuser':varuser,'form':form,'user':msg})
                else:
                    if tblcbtuser.objects.filter(session=session,klass=klass,email=user,subject=subject).count()==0:
                        tblcbtuser(session=session,klass=klass,subject=subject,user=user).save()
                        return HttpResponseRedirect('/cbt/set_user/subject/')

            else:
                user = tblcbtuser.objects.all()
                return render_to_response('CBT/entub.html',{'varuser':varuser,'form':form,'user':uza})


        else:
            form = subform()
            user = tblcbtuser.objects.all()
            return render_to_response('CBT/entub.html',{'varuser':varuser,'form':form,'user':user})


    else:
        return HttpResponseRedirect('/login')


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
    gset = userprofile.objects.filter(email__contains = term)[:10]
    suggestions = []

    if gset.count() !=0:
        for i in gset:
                suggestions.append({'label': '%s :: %s' % (i.email,i.surname), 'username': i.email})
        return suggestions
   
    else:
        suggestions.append({'label': '%s :: %s' % ('#No name','name not found'), 'username': '#Name not found!'})

        return suggestions


def getcbtklass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                kk = []
                sdic = {}
                data = Class.objects.filter(klass__startswith = acccode).order_by('id')
                for j in data:
                    j = j.klass
                    kk.append(j)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getactiveexam(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                kk = []
                sdic = {}
                data = tblcbtexams.objects.filter(status='ACTIVE')
                for j in data:
                    j = j.exam_type
                    kk.append(j)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def printper(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        uza = subjectteacher.objects.filter(teachername = varuser)
   
        if uza.count() == 0 :
            return HttpResponseRedirect('/cbt/access_denied/')

        if request.method=='POST':
            form= printform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                subject=form.cleaned_data['subject']
                user=form.cleaned_data['user']

                
                usercount=userprofile.objects.filter(email = user).count()
                if usercount == 0:
                    msg = 'INVALID USERNAME'
                    return render_to_response('CBT/entub.html',{'varuser':varuser,'form':form,'user':msg})
                else:
                    if tblcbtuser.objects.filter(session=session,klass=klass,email=user,subject=subject).count()==0:
                        tblcbtuser(session=session,klass=klass,subject=subject,user=user).save()
                        return HttpResponseRedirect('/cbt/set_user/subject/')

            else:
                user = tblcbtuser.objects.all()
                return render_to_response('CBT/entub.html',{'varuser':varuser,'form':form,'user':uza})


        else:
            form = printform()
            user = tblcbtuser.objects.all()
            return render_to_response('CBT/print.html',{'varuser':varuser,'form':form,'user':user})


    else:
        return HttpResponseRedirect('/login')




def getassessment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                kk = []
                data = tblcbtexams.objects.filter(status='ACTIVE').order_by('id')
                for j in data:
                    j = j.exam_type
                    kk.append(j)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getcbtsub(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                kk = []
            
                data = Subject.objects.filter(category=acccode).order_by('id')
                for j in data:
                    j = j.subject
                    if j not in kk:
                        kk.append(j)


                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def unautho(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        return render_to_response('CBT/unautorise.html',{'varerr':varerr,'varuser':str(varuser).upper()})
    else:
        return HttpResponseRedirect('/login/')




def getscheduledsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                klass,exam,term,session=acccode.split(':')
                data = tblcbtsubject.objects.filter(klass=klass,exam_type=exam,term=term)#.order_by('st_date','st_time').reverse()

                return render_to_response('CBT/schedule.html',{'sub':data,'klass':klass,'exam':exam,'term':term,'session':session})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def cbtstat(request):
    if "userid" in request.session:
        varuser= request.session['userid']
        user = userprofile.objects.get(email = varuser)
        uenter = user.createuser

        if uenter is False :
            return HttpResponseRedirect('/cbt/access_denied')        
        if request.method=='POST':
            form=formactive(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                exam=form.cleaned_data['exam_type']
                subject=form.cleaned_data['subject']
                klass=form.cleaned_data['sfrom']
                to=form.cleaned_data['sto']
                tdate=request.POST['st_date']
                duration=request.POST['duration']
                timeo=request.POST['timeo']
                
                                
                fromklass,ss=klass.split(' ')

                toklass,sp=to.split(' ')


#***************Handling date input*****************

                yy,mm,dd = tdate.split('-')
                dd=int(dd)
                mm=int(mm)
                yy=int(yy)
                dddt=date(yy,mm,dd)
                # dddt=date(int(tdate))

                dif = int(sp)-int(ss)
                one=[klass, to]
                two = ['JS 1', 'JS 2', 'JS 3']
                twos = ['SS 1', 'SS 2', 'SS 3']

                weekday=int(dddt.isocalendar()[1])
                # weekday=int(date(yday,mday,dday).isocalendar()[1])
                # msg=one
                # return render_to_response('CBT/selectloan.html',{'msg':msg})

                if dif == 0:
                    try:
                        tblcbtsubject.objects.get(session=session,klass=klass,exam_type=exam,
                            term=term,status='ACTIVE',subject=subject)
                    except:
                        tblcbtsubject(session=session,klass=klass,exam_type=exam,
                            term=term, st_date=dddt,status='ACTIVE', st_time=timeo,
                            duration =duration,subject=subject).save()

                elif dif == 1:
                    for k in one:
                        try:

                            tblcbtsubject.objects.get(session=session,klass=k,exam_type=exam,
                            term=term,status='ACTIVE',subject=subject)
                        except:
                            tblcbtsubject(session=session,klass=k,exam_type=exam,
                            term=term, st_date=dddt,status='ACTIVE', st_time=timeo,
                            duration =duration,subject=subject).save()


                elif dif == 2:
                    if fromklass=='SS':
                        two=twos
                    else:
                        two=two
                    for k in two:
                        try:

                            tblcbtsubject.objects.get(session=session,klass=k,exam_type=exam,
                            term=term,status='ACTIVE',subject=subject)
                        except:
                            tblcbtsubject(session=session,klass=k,exam_type=exam,
                            term=term, st_date=dddt,status='ACTIVE', st_time=timeo,
                            duration =duration,subject=subject).save()

                return render_to_response('CBT/active.html',{'varuser':varuser,'form':form})
                    # return render_to_response('CBT/active.html',{'varuser':varuser,'form':form},context_instance = RequestContext(request))
    
            else:
                return HttpResponseRedirect('/cbt/schedulling/active/')
        else:
            form = formactive()

        return render_to_response('CBT/active.html',{'varuser':varuser,'form':form})
    
    else:
        return HttpResponseRedirect('/login')


def deletesch(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    myqst=tblcbtsubject.objects.get(id = acccode)
                    return render_to_response('CBT/delschedule.html',{'user':myqst})
                
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')


def qstn(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        

        if request.method=='POST':
            form = qstnform(request.POST, request.FILES)

            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                term=form.cleaned_data['term']
                subject=form.cleaned_data['subject']
                exam_type=form.cleaned_data['exam_type']
                question=form.cleaned_data['question']
                rfile=form.cleaned_data['pix']

                if rfile is None:
                    pix = '/ax/image'
                else:
                    pix = request.FILES['pix']



                if subject == 'ENGLISH' or subject=='ENGLISH LANGUAGE':

                    
                    # msg= len(question) 
                    # return render_to_response('CBT/selectloan.html',{'msg':msg})



                    if question==" ":
                        err= 'empty questionnot allowed'
                        # msg= 'free me 1'    return render_to_response('CBT/selectloan.html',{'msg':msg})



                    else:

                        kl = tblothers.objects.filter(session=session,klass=klass,term=term, subject=subject, exam_type=exam_type, q1 =question)
                        
                        if kl.count() ==0:

                            qp =generate_blk_pin()

                            tblothers(session=session,qstcode=qp,image=pix, klass=klass,term=term, subject=subject, exam_type=exam_type, q1 =question).save()
                        
                            # msg= 'free me2' return render_to_response('CBT/selectloan.html',{'msg':msg})
            

                        else:
                            g=8

                    # return HttpResponseRedirect('/cbt/enter/question/')
                    return HttpResponseRedirect('/cbt/enter/question/others/oqstns/')


                else:

                    if tblquestion.objects.filter(instruction_to='instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).count()==0:
                        tblquestion(instruction_to=  'instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).save()
                        err= 'question saved successfully'
                    else:
                        err= 'question already exists'
                # qstn = ''
                
            else:
                err = 'spaces left not filled'
                # qstn = klass
        else:
            form = qstnform()
            err=''
            # qstn= ''
        return render_to_response('CBT/qstn.html',{'varuser':varuser,'form':form,'err':err})
    else:
        return HttpResponseRedirect('/login')

def getstudent(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term, subject,exam_type= acccode.split(':')

                stlist = []

                if term == 'First':
                    data = Student.objects.filter(admitted_class=klass,admitted_arm=arm,admitted_session=session,first_term = True,gone=False)
                if term == 'Second':
                    data = Student.objects.filter(admitted_class=klass,admitted_arm=arm,admitted_session=session,second_term = True,gone=False)
                if term == 'Third':
                    data = Student.objects.filter(admitted_class=klass,admitted_arm=arm,admitted_session=session,third_term = True,gone=False)

                for k in data:
                    ght = cbttrans.objects.filter(student=k,session=session,term=term,subject=subject,exam_type=exam_type)
                    add=ght.aggregate(Sum('score'))
                    add = add['score__sum']
                    if ght.count() == 0:
                        jk = {'student':k,'score':0}
                    else:
                        jk = {'student':k,'score':add}
                    stlist.append(jk)


                return render_to_response('CBT/printscore.html',{'data':data,
                    'stlist':stlist,'subject':subject,'exam_type':exam_type,'term':term,
                    'klass':klass,'arm':arm,'session':session})
                
            else:
                varerr='User not asigned'
                return render_to_response('assessment/notallowed.html',{'varerr':varerr})

        else:
            gdata = ""
            return render_to_response('index.html',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')



def editcbtqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                getdetails=[]
                details = tblquestion.objects.get(id = state)

                try:

                    options=tbloptions.objects.get(qstn=details)
                except:

                    options=''

                try:
                    answer= tblans.objects.get(qstn=details)

                except:
                     answer=''
                dicdetails={'options':options,'question':details,'answer':answer}
                return render_to_response('CBT/viewimage.html',{'getdetails':dicdetails,'state':options})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            getdetails = tblcontents.objects.filter(topic=id)
            return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
        return HttpResponseRedirect('/login/')



def editcbtpix(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                getdetails=[]
                details = tblquestion.objects.get(id = state)

                try:

                    options=tbloptions.objects.get(qstn=details)
                except:

                    options=''

                try:
                    answer= tblans.objects.get(qstn=details)

                except:
                     answer=''
                dicdetails={'options':options,'question':details,'answer':answer}
                return render_to_response('CBT/putimage.html',{'getdetails':dicdetails,'state':options})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            getdetails = tblcontents.objects.filter(topic=id)
            return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
        return HttpResponseRedirect('/login/')







def getcbtqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')


                if subject=='ENGLISH' or subject=='ENGLISH LANGUAGE':

                    try:

                        qqq=tblcomprehension.objects.get(session=session,                        
                            term=term,
                            klass=klass,
                            subject=subject,
                            exam_type=exam_type)

                    except:
                        qqq=[]


                    return render_to_response('CBT/english2.html',{'qq':qqq,'term':term,
                        'subject':subject,
                        'exam':exam_type,
                        'klass':klass,'session':session})


                else:


                    myqst=[]
                    
                    myqst=tblquestion.objects.filter(session=session,
                        term=term,
                        klass=klass,
                        subject=subject,
                        exam_type=exam_type).order_by('klass')


                    km=0

                    qt=[]

                    for n in myqst:
                        ans =tbloptions.objects.filter(qstn =n)

                        fv= ans.count()

                        if fv ==0:
                            km =0

                            ans = tbloptioni.objects.filter(qstn=n)
                            fv =ans.count()

                            if fv ==0:
                                km=0
                            
                            elif fv==1:
                                km = 1

                        elif fv ==1:
                            km=1

                        if km ==0:
                            tr = {'question':n, 'options':'NOT YET','id':n.id}
                        elif km ==1:
                            tr = {'question':n, 'options':'YES','id':n.id}

                        qt.append(tr)


                    return render_to_response('CBT/myqst.html',{'myqst':qt,'term':term,
                        'subject':subject,
                        'exam':exam_type,
                        'klass':klass,'session':session})

        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getcbtengqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                
            
                comp=tblcomprehension.objects.filter(session=session,                        
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam_type)
                q=[]
                
                if comp.count()==1:
                    comp=tblcomprehension.objects.filter(session=session,                        
                        term=term,
                        klass=klass,
                        subject=subject,
                        exam_type=exam_type)

                    for k in comp:
                        questions=tblcomprehensionqst.objects.filter(comprehension = k)

                        hg= {'p':k,'q':questions}
                        q.append(hg)
                    

                    return render_to_response('CBT/objqst.html',{'quest':q,'term':term,
                        'subject':subject,
                        'exam':exam_type,
                        'klass':klass,
                        'session':session})
                else:
                    msg =' no comprehension passage found'
                    return render_to_response('CBT/nill.html',{'msg':msg})


            else:
                return HttpResponseRedirect('/login/')
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


###ENgkish


def english(request):
    if  "userid" in request.session:

        if request.method == 'POST':
            term = request.POST['term']
            session = request.POST['session']
            klass = request.POST['klass']
            subject = request.POST['subject']
            exam = request.POST['exam']
            p1 =request.POST['p1']
            p2 =request.POST['p2']
            p3 =request.POST['p3']
            p4 =request.POST['p4']

            
            try:
                qq=tblcomprehension.objects.get(session=session,                        
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam)

                qq.p1 =p1
                qq.p2 =p2
                qq.p3 =p3
                qq.p4 =p4
                qq.save()


            except:

                tblcomprehension(session=session,                        
                    term=term,
                    klass=klass,
                    subject=subject,
                    p1=p1, p2=p2,
                    p3=p3,p4=p4,
                    exam_type=exam).save()


            return HttpResponseRedirect('/cbt/enter/question/')

        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')



def comprqstn(request):
    if 'userid' in request.session:
        varuser = request.session['userid']

        form = compform()

        err = 'saved successfully'




        return render_to_response('CBT/compqst.html',{'varuser':varuser,'form':form,'err':err})
    else:
        return HttpResponseRedirect('/login')


def bblock(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        if request.method=='POST':
            form = qstnform(request.POST, request.FILES)

            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                term=form.cleaned_data['term']
                subject=form.cleaned_data['subject']
                exam_type=form.cleaned_data['exam_type']
                question=form.cleaned_data['question']
                rfile=form.cleaned_data['pix']

                if rfile is None:
                    pix = '/ax/image'
                else:
                    pix = request.FILES['pix']

                if tblquestion.objects.filter(instruction_to='instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).count()==0:
                    tblquestion(instruction_to=  'instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).save()
                    err= 'question saved successfully'
                else:
                    err= 'question already exists'
                # qstn = ''
                
            else:
                err = 'spaces left not filled'
                # qstn = klass
        else:
            form = qstnform()
            err=''
            # qstn= ''
        return render_to_response('CBT/cmpblk.html',{'varuser':varuser,'form':form,'err':err})
    else:
        return HttpResponseRedirect('/login')


def bblockqstn(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        if request.method=='POST':
            form = qstnform(request.POST, request.FILES)

            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                term=form.cleaned_data['term']
                subject=form.cleaned_data['subject']
                exam_type=form.cleaned_data['exam_type']
                question=form.cleaned_data['question']
                rfile=form.cleaned_data['pix']

                if rfile is None:
                    pix = '/ax/image'
                else:
                    pix = request.FILES['pix']

                if tblquestion.objects.filter(instruction_to='instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).count()==0:
                    tblquestion(instruction_to=  'instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).save()
                    err= 'question saved successfully'
                else:
                    err= 'question already exists'
                # qstn = ''
                
            else:
                err = 'spaces left not filled'
                # qstn = klass
        else:
            form = qstnform()
            err=''
            # qstn= ''
        return render_to_response('CBT/cmpqst.html',{'varuser':varuser,'form':form,'err':err})
    else:
        return HttpResponseRedirect('/login')


def otherqstn(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        if request.method=='POST':
            form = qstnform(request.POST, request.FILES)

            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                term=form.cleaned_data['term']
                subject=form.cleaned_data['subject']
                exam_type=form.cleaned_data['exam_type']
                question=form.cleaned_data['question']
                rfile=form.cleaned_data['pix']

                if rfile is None:
                    pix = '/ax/image'
                else:
                    pix = request.FILES['pix']

                if tblquestion.objects.filter(instruction_to='instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).count()==0:
                    tblquestion(instruction_to=  'instruction',session=session,klass=klass,section='A',term=term,subject=subject,exam_type=  exam_type,qstn =question,topic='topic', image=pix).save()
                    err= 'question saved successfully'
                else:
                    err= 'question already exists'
                # qstn = ''
                
            else:
                err = 'spaces left not filled'
                # qstn = klass
        else:
            form = qstnform()
            err=''
            # qstn= ''
        return render_to_response('CBT/otherqst.html',{'varuser':varuser,'form':form,'err':err})
    else:
        return HttpResponseRedirect('/login')










def compquest(request):
    if  "userid" in request.session:



        if request.method == 'POST':
            term = request.POST['term']
            session = request.POST['session']
            klass = request.POST['klass']
            subject = request.POST['subject']
            exam = request.POST['exam']

            q1 =request.POST['question']

            # if q1 =="":



            try:

                comp=tblcomprehension.objects.get(session=session,                        
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam)

                code= generate_blk_pin()

            
                tblcomprehensionqst(comprehension =comp,q1=q1,code1='C',qstcode=code).save()

            except:
                f=0
            # else:
            #     f=0
                    

            return HttpResponseRedirect('/cbt/enter/question/comprehension/')


        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')



def getcbtengblk(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')

                
            
                comp=tblblock.objects.filter(session=session,                        
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam_type)
                

                return render_to_response('CBT/cbtblk.html',{'q':comp,'term':term,
                    'subject':subject,
                    'exam':exam_type,
                    'klass':klass,
                    'session':session})
            else:
                msg =' no comprehension passage found'
                return render_to_response('CBT/nill.html',{'msg':msg})


        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')




def allblkq(request):
    if  "userid" in request.session:



        if request.method == 'POST':
            term = request.POST['term']
            session = request.POST['session']
            klass = request.POST['klass']
            subject = request.POST['subject']
            exam = request.POST['exam']
            inst =request.POST['instruction']

            if inst != "":
                pin =generate_blk_pin()
        
                tblblock(session=session,                        
                    term=term,
                    klass=klass,
                    code=pin,
                    subject=subject,
                    exam_type=exam,instruction=inst).save()


            return HttpResponseRedirect('/cbt/enter/question/bblock/')


        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')


def editallblkq(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
        
                instr=tblblock.objects.get(code=acccode)
                return render_to_response('CBT/dlkedit.html',{'getdetails':instr})

        else:
            return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def editallinstr(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
        
                instr=tblblock.objects.get(code=acccode)
                return render_to_response('CBT/dlkedit2.html',{'getdetails':instr})

        else:
            return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')



def instchh(request,vid):
    if  "userid" in request.session:
        inst =request.POST['getdetails']
        ing = tblblock.objects.get(code=vid)
        ing.instruction=inst
        ing.save()
        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')


def editblktxtqst(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
        
                instr=tblblockquestion.objects.get(qstcode=acccode)

                if instr.image=='studentpix/user.png':
                    return render_to_response('CBT/editblkqstpop.html',{'getdetails':instr})
                else:
                    return render_to_response('CBT/editblkqstpopi.html',{'getdetails':instr})

        else:
            return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def editsaveblk(request,vid):
    if  "userid" in request.session:
        if request.method=='POST':
            inst =request.POST['getdetails']
            ing = tblblockquestion.objects.get(qstcode=vid)
            ing.q1=inst
            ing.save()
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')


def editsaveblki(request,vid):
    if  "userid" in request.session:
        if request.method=='POST':
            if  request.FILES:
                img =request.FILES['qstfile']
                ing = tblblockquestion.objects.get(qstcode=vid)
                ing.image=img
                ing.save()

            else:
                msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})

        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def editqstbblk(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblblockquestion.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionblk.objects.get(qstn=details).a
                        return render_to_response('CBT/blkeditpop.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionblki.objects.get(qstn=details).a

                        return render_to_response('CBT/blkeditimage.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')





def editoptiobimagelkA(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']


                old_optionA =request.POST['optionA']


                box,ext = old_optionA.split('/')

                details = tblblockquestion.objects.get(qstcode = vid)
                
                options=tbloptionblki.objects.get(qstn=details)

                ans2 = tblansblk.objects.get(qstn=details)
                ans = ans2.ans


                options.a =new_optionA
                options.save()

                if old_optionA == ans:

                    options=tbloptionblki.objects.get(qstn=details)
                    new_optionA = options.a
                    ans2.ans=str(box) + '/' + str(new_optionA)
                    ans2.save()



            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def editoptioblkA(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblblockquestion.objects.get(qstcode = vid)
            
            options=tbloptionblk.objects.get(qstn=details)

            ans2 = tblansblk.objects.get(qstn=details)
            ans = ans2.ans

            options.a =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans =new_optionA
                ans2.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')





def editqstbblkb(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblblockquestion.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionblk.objects.get(qstn=details).b
                        return render_to_response('CBT/blkeditpopB.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionblki.objects.get(qstn=details).b

                        return render_to_response('CBT/blkeditimageB.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')



def editoptiobimagelkB(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']

                old_optionA =request.POST['optionA']

                box,ext = old_optionA.split('/')

                details = tblblockquestion.objects.get(qstcode = vid)
                
                options=tbloptionblki.objects.get(qstn=details)

                ans2 = tblansblk.objects.get(qstn=details)
                ans = ans2.ans


                options.b =new_optionA
                options.save()

                if old_optionA == ans:
                    options=tbloptionblki.objects.get(qstn=details)
                    new_optionA = options.b
                    ans2.ans=new_optionA
                    ans2.save()


            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')



def editoptioblkB(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']


            old_optionA = request.POST['getdetails']

            details = tblblockquestion.objects.get(qstcode = vid)
            
            options=tbloptionblk.objects.get(qstn=details)

            ans2 = tblansblk.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.b =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.b =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')


        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')






def editqstbblkc(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            


                try:
                    details = tblblockquestion.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionblk.objects.get(qstn=details).c
                        return render_to_response('CBT/blkeditpopC.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionblki.objects.get(qstn=details).c

                        return render_to_response('CBT/blkeditimageC.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})



def editoptioblkC(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']


            old_optionA = request.POST['getdetails']

            details = tblblockquestion.objects.get(qstcode = vid)


            
            options=tbloptionblk.objects.get(qstn=details)

            ans2 = tblansblk.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.c =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.c =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')




def editoptiobimagelkC(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']

                old_optionA =request.POST['optionA']

                box,ext = old_optionA.split('/')

                details = tblblockquestion.objects.get(qstcode = vid)
                
                options=tbloptionblki.objects.get(qstn=details)

                ans2 = tblansblk.objects.get(qstn=details)
                ans = ans2.ans


                options.c =new_optionA
                options.save()

                if old_optionA == ans:
                    options=tbloptionblki.objects.get(qstn=details)
                    new_optionC = options.c
                    ans2.ans=new_optionC
                    ans2.save()


            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def editqstbblkd(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            


                try:
                    details = tblblockquestion.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionblk.objects.get(qstn=details).d
                        return render_to_response('CBT/blkeditpopD.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionblki.objects.get(qstn=details).d

                        return render_to_response('CBT/blkeditimageD.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})




def editoptioblkD(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblblockquestion.objects.get(qstcode = vid)


            
            options=tbloptionblk.objects.get(qstn=details)

            ans2 = tblansblk.objects.get(qstn=details)
            ans = ans2.ans


            options.d =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans=new_optionA
                ans2.save()




            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def editoptiobimagelkD(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']

                old_optionA =request.POST['optionA']

                box,ext = old_optionA.split('/')

                details = tblblockquestion.objects.get(qstcode = vid)
                
                options=tbloptionblki.objects.get(qstn=details)

                ans2 = tblansblk.objects.get(qstn=details)
                ans = ans2.ans


                options.d =new_optionA
                options.save()

                if old_optionA == ans:
                    options=tbloptionblki.objects.get(qstn=details)
                    new_optionD = options.d
                    ans2.ans=new_optionD
                    ans2.save()


            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')


def editblkans(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                try:
                    details = tblblockquestion.objects.get(qstcode = state)
                    ans=tblansblk.objects.get(qstn=details)

                    try:
                        options=tbloptionblk.objects.get(qstn=details)
                        return render_to_response('CBT/aditblkans.html',{'ans':ans,'qst':details,'opt':options})
                    except:
                        options=tbloptionblki.objects.get(qstn=details)
                        return render_to_response('CBT/aditblkansi.html',{'ans':ans,'qst':details,'opt':options})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')

def changeblkans(request,vid):

    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]


            if 'gender' in request.POST:
                answer = request.POST['gender']
                details = tblblockquestion.objects.get(qstcode=vid)

                ans=tblansblk.objects.get(qstn=details)


                try:
                    options=tbloptionblk.objects.get(qstn=details)
                except:
                    options=tbloptionblki.objects.get(qstn=details)
                


                if answer == options.a:
                    ppp = 'A'
                if answer == options.b:
                    ppp = 'B'

                if answer == options.c:
                    ppp = 'C'

                if answer == options.d:
                    ppp = 'D'



                ans.ans = answer
                ans.option=ppp
                ans.save()


        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')






def editoptodaspop(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblothers.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionsothers.objects.get(qstn=details).a
                        return render_to_response('CBT/otherseditpop.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionothersi.objects.get(qstn=details).a

                        return render_to_response('CBT/otheditimage.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')







def editoptionodaA(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblothers.objects.get(qstcode = vid)
            
            options=tbloptionsothers.objects.get(qstn=details)

            ans2 = tblansothers.objects.get(qstn=details)
            ans = ans2.ans

            options.a =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans =new_optionA
                ans2.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def chngoptiobimageA(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']


                old_optionA =request.POST['optionA']


                box,ext = old_optionA.split('/')

                details = tblothers.objects.get(qstcode = vid)
                
                options=tbloptionothersi.objects.get(qstn=details)

                ans2 = tblansothers.objects.get(qstn=details)
                ans = ans2.ans


                options.a =new_optionA
                options.save()

                if old_optionA == ans:

                    options=tbloptionothersi.objects.get(qstn=details)
                    new_optionA = options.a
                    ans2.ans=new_optionA
                    ans2.save()



            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')






def editoptodaspopB(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblothers.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionsothers.objects.get(qstn=details).b
                        return render_to_response('CBT/otherseditpopB.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionothersi.objects.get(qstn=details).b

                        return render_to_response('CBT/otheditimageB.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')







def editoptionodaB(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblothers.objects.get(qstcode = vid)
            
            options=tbloptionsothers.objects.get(qstn=details)

            ans2 = tblansothers.objects.get(qstn=details)
            ans = ans2.ans

            options.b =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans =new_optionA
                ans2.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def chngoptiobimageB(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']


                old_optionA =request.POST['optionA']


                box,ext = old_optionA.split('/')

                details = tblothers.objects.get(qstcode = vid)
                
                options=tbloptionothersi.objects.get(qstn=details)

                ans2 = tblansothers.objects.get(qstn=details)
                ans = ans2.ans


                options.b =new_optionA
                options.save()

                if old_optionA == ans:

                    options=tbloptionothersi.objects.get(qstn=details)
                    new_optionA = options.b
                    ans2.ans=new_optionA
                    ans2.save()



            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')







def editoptodaspopC(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblothers.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionsothers.objects.get(qstn=details).c
                        return render_to_response('CBT/otherseditpopC.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionothersi.objects.get(qstn=details).c

                        return render_to_response('CBT/otheditimageC.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')







def editoptionodaC(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblothers.objects.get(qstcode = vid)
            
            options=tbloptionsothers.objects.get(qstn=details)

            ans2 = tblansothers.objects.get(qstn=details)
            ans = ans2.ans

            options.c =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans =new_optionA
                ans2.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def chngoptiobimageC(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']


                old_optionA =request.POST['optionA']


                box,ext = old_optionA.split('/')

                details = tblothers.objects.get(qstcode = vid)
                
                options=tbloptionothersi.objects.get(qstn=details)

                ans2 = tblansothers.objects.get(qstn=details)
                ans = ans2.ans


                options.c =new_optionA
                options.save()

                if old_optionA == ans:

                    options=tbloptionothersi.objects.get(qstn=details)
                    new_optionA = options.c
                    ans2.ans=new_optionA
                    ans2.save()


            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')








def editoptodaspopD(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            

                try:
                    details = tblothers.objects.get(qstcode=state)
                    try:
                        optionA=tbloptionsothers.objects.get(qstn=details).d
                        return render_to_response('CBT/otherseditpopD.html',{'a':optionA,'code':state})
                    
                    except:
                        optionA=tbloptionothersi.objects.get(qstn=details).d

                        return render_to_response('CBT/otheditimageD.html',{'a':optionA,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})
       
        else:
            return HttpResponseRedirect('/login/')







def editoptionodaD(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            old_optionA = request.POST['optionA']


            new_optionA = request.POST['getdetails']

            details = tblothers.objects.get(qstcode = vid)
            
            options=tbloptionsothers.objects.get(qstn=details)

            ans2 = tblansothers.objects.get(qstn=details)
            ans = ans2.ans

            options.d =new_optionA
            options.save()


            if old_optionA == ans:
                ans2.ans =new_optionA
                ans2.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def chngoptiobimageD(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            if  request.FILES:

                new_optionA = request.FILES['qstfl']


                old_optionA =request.POST['optionA']


                box,ext = old_optionA.split('/')

                details = tblothers.objects.get(qstcode = vid)
                
                options=tbloptionothersi.objects.get(qstn=details)

                ans2 = tblansothers.objects.get(qstn=details)
                ans = ans2.ans


                options.d =new_optionA
                options.save()

                if old_optionA == ans:

                    options=tbloptionothersi.objects.get(qstn=details)
                    new_optionA = options.d
                    ans2.ans=new_optionA
                    ans2.save()



            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')





























def editotherans(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                try:
                    details = tblothers.objects.get(qstcode = state)
                    ans=tblansothers.objects.get(qstn=details)

                    try:
                        options=tbloptionsothers.objects.get(qstn=details)
                        return render_to_response('CBT/aditodaans.html',{'ans':ans,'qst':details,'opt':options})
                    except:
                        options=tbloptionothersi.objects.get(qstn=details)
                        return render_to_response('CBT/aditotheransi.html',{'ans':ans,'qst':details,'opt':options})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')

def changeotherans(request,vid):

    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]


            if 'gender' in request.POST:
                answer = request.POST['gender']
                details = tblothers.objects.get(qstcode=vid)

                ans=tblansothers.objects.get(qstn=details)


                try:
                    options=tbloptionsothers.objects.get(qstn=details)
                except:
                    options=tbloptionothersi.objects.get(qstn=details)
                


                if answer == options.a:
                    ppp = 'A'
                if answer == options.b:
                    ppp = 'B'

                if answer == options.c:
                    ppp = 'C'

                if answer == options.d:
                    ppp = 'D'



                ans.ans = answer
                ans.option=ppp
                ans.save()


        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')















def editqstodaspop(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
        
                instr=tblothers.objects.get(qstcode=acccode)
                return render_to_response('CBT/othereditpop.html',{'getdetails':instr})

        else:
            return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def editqstodas(request,vid):
    if  "userid" in request.session:
        inst =request.POST['getdetails']
        ing = tblothers.objects.get(qstcode=vid)
        ing.q1=inst
        ing.save()
        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def editqstodasimagepop(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
        
                instr=tblothers.objects.get(qstcode=acccode)
                return render_to_response('CBT/othereditimagepop.html',{'getdetails':instr})

        else:
            return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def editqstodasimage(request,vid):
    if  "userid" in request.session:
        if request.method =='POST':
            if 'qst' in request.FILES:
                inst =request.FILES['qst']
                ing = tblothers.objects.get(qstcode=vid)
                ing.image = inst
                ing.save()

            else:
                msg='Select a file'                    
                return render_to_response('CBT/selectloan.html',{'msg':msg})


        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')


def cngblkqstt2(request,vid):
    if  "userid" in request.session:
        inst =request.POST['getdetails']
        ing = tblcomprehensionqst.objects.get(qstcode=vid)
        ing.q1=inst
        ing.save()
        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')



def installblkq(request,vid):
    if  "userid" in request.session:
        inst =request.POST['getdetails']
        ing = tblblock.objects.get(code=vid)
        ing.instruction=inst
        ing.save()
        return HttpResponseRedirect('/cbt/enter/question/bblock/')

    else:
        return HttpResponseRedirect('/login/')


def getblockqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')

                blk=tblblock.objects.filter(session=session,
                    term=term,
                    klass=klass,
                    exam_type=exam_type,
                    subject=subject)

                allqst=[]

                for k in blk:
                    qst = tblblockquestion.objects.filter(block=k)
                    lk={'inst':k,'qst':qst}
                    allqst.append(lk)

                return render_to_response('CBT/blkqst.html',{'q':allqst,
                    'term':term,
                    'subject':subject,
                    'Exam':exam_type,
                    'klass':klass,
                    'session':session})


            return HttpResponseRedirect('/cbt/enter/question/')

        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')


def addsomblkqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode

                blk=tblblock.objects.get(code=state)

                return render_to_response('CBT/addblkqst.html',{'q':blk})


            return HttpResponseRedirect('/cbt/enter/question/')

        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')


def blkuestion(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            term = request.POST['term']
            session = request.POST['session']
            klass = request.POST['klass']
            subject = request.POST['subject']
            exam = request.POST['exam']
            q = request.POST['q'] #quest



            fh =tblblock.objects.get(code=vid)

            gp = generate_blk_pin()


            if q == "" :

                if request.FILES:
                    pix=request.FILES['qfilem']
                    tblblockquestion(block=fh,q1=q,image=pix,qstcode=gp).save()

                else:
                    pix= 'studentpix/user.png'

            else:                
            
                tblblockquestion(block=fh,q1=q,qstcode=gp).save()


            return HttpResponseRedirect('/cbt/enter/question/bblock/qstns/') 

        else:
            return HttpResponseRedirect('/cbt/enter/question/')

    else:
        return HttpResponseRedirect('/login/')



def blkqstedit(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode

                qst = tblblockquestion.objects.get(id=state)

                return render_to_response('CBT/chngqst.html',{'q':qst})

            else:

                return HttpResponseRedirect('/cbt/enter/question/')

        else:
            return HttpResponseRedirect('/cbt/enter/question/')



    else:
        return HttpResponseRedirect('/login/')




"""
def ff():
    fs=0
    if "userid" in request.session:
            if request.method=='POST':
                if request.FILES:                
                    if 'option' in request.POST: #if you selected an option
                        a=request.FILES['filea']
                        b=request.FILES['fileb']
                        c=request.FILES['filec']
                        d=request.FILES['filed']
                        option = request.POST['option']

                        if a=='' or b=='' or c=='' or d=='':
                            return HttpResponseRedirect('/cbt/options/dgfgeg/gukyur/')
                        
                        qst=tblblockquestion.objects.get(id=vid)
                        
                        tbloptionblki(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()


"""


def getothers(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                # myqst=[]

                if subject=='ENGLISH' or subject=='ENGLISH LANGUAGE':

                    qqq=tblothers.objects.filter(session=session,                        
                        term=term,
                        klass=klass,
                        subject=subject,
                        exam_type=exam_type)


                    km=0

                    qt=[]

                    for n in qqq:
                        ans =tbloptionothersi.objects.filter(qstn =n)

                        fv= ans.count()

                        if fv ==0:
                            km =0

                            ans = tbloptionsothers.objects.filter(qstn=n)
                            fv =ans.count()

                            if fv ==0:
                                km=0
                            
                            elif fv==1:
                                km = 1

                        elif fv ==1:
                            km=1

                        if km ==0:
                            tr = {'question':n, 'options':'NOT YET','id':n.id}
                        elif km ==1:
                            tr = {'question':n, 'options':'YES','id':n.id}

                        qt.append(tr)





                    return render_to_response('CBT/others.html',{'qq':qt,'term':term,
                        'subject':subject,
                        'exam':exam_type,
                        'klass':klass,'session':session})

                else:
                    return render_to_response('CBT/myqst.html',{'myqst':myqst,
                    'term':term,'subject':subject,'exam':exam_type,'klass':klass,'session':session})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')




def popeditx(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                getdetails=[]

                details = tblothers.objects.get(id = state)

                try:

                    options=tbloptions.objects.get(qstn=details)
                except:

                    options=''

                try:
                    answer= tblans.objects.get(qstn=details)

                except:
                     answer=''
                dicdetails={'options':options,'question':details,'answer':answer}
                return render_to_response('CBT/otherpop.html',{'getdetails':dicdetails,'state':options})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            getdetails = tblcontents.objects.filter(topic=id)
            return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
        return HttpResponseRedirect('/login/')




def popengl(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            if request.FILES:
                a=request.FILES['filetoupload']
                qt = tblothers.objects.get(id=vid)
                qt.image=a
                qt.save()
        return HttpResponseRedirect('/cbt/enter/question/others/oqstns/')
    else:
        return HttpResponseRedirect('/login/')




def blkoption(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                details = tblblockquestion.objects.get(id = state)


                try:
                    options= tbloptionblki.objects.get(qstn=details)
                    answer= tblansblk.objects.get(qstn=details)
                    dicdetails={'options':options,'question':details,'answer':answer}                    
                    return render_to_response('CBT/blkimage.html',{'getdetails':dicdetails})

                except:

                    opt= tbloptionblk.objects.filter(qstn=details)
                    if opt.count()>0:
                        options= tbloptionblk.objects.get(qstn=details)
                        answer= tblansblk.objects.get(qstn=details)
                        dicdetails={'options':options,'question':details,'answer':answer}                    
                        return render_to_response('CBT/blkqstpop.html',{'getdetails':dicdetails})

                    else:
                        return render_to_response('CBT/chooseblk.html',{'state':state})

    else:
        return HttpResponseRedirect('/login/')



def blktextts(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblblockquestion.objects.get(id=vid)
            session=qst.block.session
            subject=qst.block.subject
            term=qst.block.term
            exam=qst.block.exam_type
            code=qst.id

            return HttpResponseRedirect('/cbt/input_text/blkqst/%s/%s/%s/%s/'%(code,
                str(session).replace('/','k'),
                term,
                # str(subject).replace(' ','w'),
                str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')




def save_blktext(request,code,session,term,exam):
    session = str(session).replace('k','/')
    term = str(term).replace('w',' ')
    # subject = str(subject).replace('w',' ')
    exam = str(exam).replace('p',' ')

    if request.method == 'GET':
        getdetails=[]
        details = tblblockquestion.objects.get(id = code)

        try:
            options=tbloptionblk.objects.get(qstn=details)
        except:
            options=''
        try:
            answer= tblansblk.objects.get(qstn=details)

        except:
             answer=''
            
        dicdetails={'options':options,'question':details,'answer':answer}

        return render_to_response('CBT/enterblkqsr.html',{'getdetails':dicdetails,})
    

def myblkoptions(request,vid):
    if "userid" in request.session:
        varuser=request.session['userid']
        if 'option' in request.POST:
            if request.method=='POST':
                a=request.POST['optiona']
                b=request.POST['optionb']
                c=request.POST['optionc']
                d=request.POST['optiond']



                qst=tblblockquestion.objects.get(id=vid)

                tbloptionblk(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()
                option = request.POST['option']

                gh = tbloptionblk.objects.get(qstn=qst)

                a = gh.a
                b = gh.b
                c= gh.c
                d= gh.d



                if option=='A':
                    tblansblk (ans =a,option=option,qstn=qst).save()
                elif option=='B':
                    tblansblk(ans =b,option=option,qstn=qst).save()
                elif option=='C':
                    tblansblk(ans =c,option=option,qstn=qst).save()
                elif option=='D':
                    tblansblk(ans =d,option=option,qstn=qst).save()
                g= 'my name is mathew'
                return HttpResponseRedirect('/cbt/options/')# 

            else:
                return HttpResponseRedirect('/login/')
        else:
            f = 'my name is black'
            return HttpResponseRedirect('/cbt/options/')
    else:
        return HttpResponseRedirect('/login/')

def imagesp(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblblockquestion.objects.get(id=vid)
            session=qst.block.session
            klass='JS 1'
            subject=qst.block.subject
            term=qst.block.term
            exam=qst.block.exam_type
            code=qst.id

            return HttpResponseRedirect('/cbt/blkqst/input_images/%s/%s/%s/%s/%s/%s/'%(code,
                str(session).replace('/','k'),
                str(klass).replace(' ','m'),
                term,
                str(subject).replace(' ','w'),
                str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')


def save_blkimages(request,code,session,klass, term,subject,exam):
    session = str(session).replace('k','/')
    klass = str(klass).replace('m',' ')
    subject = str(subject).replace('w',' ')
    exam = str(exam).replace('p',' ')

    if request.method == 'GET':
        getdetails=[]
        details = tblblockquestion.objects.get(id = code)
            
        dicdetails={'question':details}

        return render_to_response('CBT/qstimage.html',{'getdetails':dicdetails})





def imagesothers(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblothers.objects.get(qstcode=vid)
            session=qst.session
            subject=qst.subject
            term=qst.term
            exam=qst.exam_type
            code=qst.qstcode

            return HttpResponseRedirect('/cbt/otherqst/input_otherimages/%s/%s/%s/%s/%s/'%(code,
                str(session).replace('/','k'),
                term,
                str(subject).replace(' ','w'),
                str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')





def odaoptionsimage(request,vid):
    if "userid" in request.session:
            if request.method=='POST':
                if request.FILES:

                    if 'option' in request.POST: #if you selected an option
                        a=request.FILES['filea']
                        b=request.FILES['fileb']
                        c=request.FILES['filec']
                        d=request.FILES['filed']
                        option = request.POST['option']
                        
                        qst=tblothers.objects.get(qstcode=vid)
                        
                        tbloptionothersi(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()
                        gh = tbloptionothersi.objects.get(qstn=qst)

                        a = gh.a
                        b = gh.b
                        c= gh.c
                        d= gh.d


                        if option=='A':
                            tblansothers(ans =a,option=option,qstn=qst).save()
                        elif option=='B':
                            tblansothers(ans =b,option=option,qstn=qst).save()
                        elif option=='C':
                            tblansothers(ans =c,option=option,qstn=qst).save()
                        elif option=='D':
                            tblansothers(ans =d,option=option,qstn=qst).save()

                        return HttpResponseRedirect('/cbt/options/')
                    else:
                        return HttpResponseRedirect('/cbt/options/')
                else:
                    return HttpResponseRedirect('/cbt/options/')
            else:

                return HttpResponseRedirect('/login/')

            
    else:
        return HttpResponseRedirect('/login/')


def blkoptionsimage(request,vid):
    if "userid" in request.session:
            if request.method=='POST':
                if request.FILES:                
                    if 'option' in request.POST: #if you selected an option
                        a=request.FILES['filea']
                        b=request.FILES['fileb']
                        c=request.FILES['filec']
                        d=request.FILES['filed']
                        option = request.POST['option']

                        if a=='' or b=='' or c=='' or d=='':
                            return HttpResponseRedirect('/cbt/options/dgfgeg/gukyur/')
                        
                        qst=tblblockquestion.objects.get(id=vid)
                        
                        tbloptionblki(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()

                        gh = tbloptionblki.objects.get(qstn=qst)

                        a = gh.a
                        b = gh.b
                        c= gh.c
                        d= gh.d


                        if option=='A':
                            tblansblk(ans =a,option=option,qstn=qst).save()
                        elif option=='B':
                            tblansblk(ans =b,option=option,qstn=qst).save()
                        elif option=='C':
                            tblansblk(ans =c,option=option,qstn=qst).save()
                        elif option=='D':
                            tblansblk(ans =d,option=option,qstn=qst).save()

                        return HttpResponseRedirect('/cbt/options/')
                    else:
                        return HttpResponseRedirect('/cbt/options/')
                else:
                    return HttpResponseRedirect('/cbt/options/')
            else:

                return HttpResponseRedirect('/login/')

            
    else:
        return HttpResponseRedirect('/login/')



def my_scripts(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        if request.method=='POST':
            form = stuform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                try:
                    chk=tblcf.objects.get(session=session,term=term)
                    chkdate = chk.deadline
                except:
                    chkdate = date


                data=Student.objects.get(admissionno=varuser.upper(),admitted_session=currse,gone=False)
                ex=tblcbtexams.objects.get(status='ACTIVE')

                replist=[]
                myexam = donesubjects.objects.filter(session=currse,exam_type=ex.exam_type,student=data,term=term)
                replist=[str(k.subject) for k in myexam]
                
                scriptlist=[]
                for stusub in replist:
                    script=cbttrans.objects.filter(term=term,student=data,session=currse,subject=stusub,exam_type=ex.exam_type).order_by('question')
                    scripty=script.aggregate(Sum('score'))
                    add = scripty['score__sum']
                    total=script.count()             
                    
                    optionlist=[]
                    for kp in script:
                        quest=tblquestion.objects.get(id=kp.qstcode,term=term,session=currse,klass=data.admitted_class,exam_type=ex.exam_type,subject=stusub)
                        answer=tblans.objects.get(qstn=quest)

                        k = tbloptions.objects.filter(qstn=quest).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=quest)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=quest)
                            image='low'

                        optdic={'question':kp,'options':opt,'answer':answer,'image':image}
                        optionlist.append(optdic)

                    newlist={'subject':stusub,'details':optionlist,'total':total,'add':add,}
                    scriptlist.append(newlist)

                   #### REMOVE LATER *************************8
                    # myexam.delete()
                    # script.delete()

                return render_to_response('CBT/allscripts.html',{'getdetails':scriptlist,'term':term,'data':data})

        else:
            form= stuform()
        return render_to_response('CBT/myscripts.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')




def optajax(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode

                    getdetails=[]


                    details = tblquestion.objects.get(id = state)

                    try:

                        options=tbloptions.objects.get(qstn=details)

                    except:

                        options=''

                    try:
                        answer= tblans.objects.get(qstn=details)

                    except:
                         answer=''
                        
                    dicdetails={'options':options,'question':details,'answer':answer}

                    return render_to_response('CBT/enteropt.html',{'getdetails':dicdetails,'state':options})
                    # return render_to_response('CBT/enteropt.html',{'getdetails':getdetails,'state':options})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                getdetails = tblcontents.objects.filter(topic=id)
                return render_to_response('lesson/entersub.html',{'gdata':getdetails})
        else:
            return HttpResponseRedirect('/login/')


def chooseopt(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                details = tblquestion.objects.get(id = state)


                try:
                    options= tbloptioni.objects.get(qstn=details)
                    answer= tblans.objects.get(qstn=details)
                    dicdetails={'options':options,'question':details,'answer':answer}                    
                    return render_to_response('CBT/enteropt2.html',{'getdetails':dicdetails})

                except:
                    opt= tbloptions.objects.filter(qstn=details)
                    if opt.count()>0:
                        options= tbloptions.objects.get(qstn=details)
                        answer= tblans.objects.get(qstn=details)
                        dicdetails={'options':options,'question':details,'answer':answer}                    
                        return render_to_response('CBT/enteroption.html',{'getdetails':dicdetails})

                    else:
                        return render_to_response('CBT/choose.html',{'state':state})

    else:
        return HttpResponseRedirect('/login/')


def enlarge(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                details = tblquestion.objects.get(id = state)
                return render_to_response('CBT/enlarge.html',{'getdetails':details,})


    else:
        return HttpResponseRedirect('/login/')






def doentry(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    try:

                        options=tbloptions.objects.get(qstn=details)

                    except:

                        options=''

                    try:
                        answer= tblans.objects.get(qstn=details)

                    except:
                         answer=''          
                    dicdetails={'options':options,'question':details,'answer':answer}

            return render_to_response('CBT/edditall.html',{'getdetails':dicdetails,'state':options})
        else:
            return HttpResponseRedirect('/login/')


def sdfgsf(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    try:

                        options=tbloptions.objects.get(qstn=details)

                    except:

                        options=''

                    try:
                        answer= tblans.objects.get(qstn=details)

                    except:
                         answer=''          
                    dicdetails={'options':options,'question':details,'answer':answer}

            return render_to_response('CBT/editimagedialog.html',{'getdetails':dicdetails,'state':options})
        else:
            return HttpResponseRedirect('/login/')








def editqst(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode

                    getdetails=[]


                    details = tblquestion.objects.get(id = state)

                    try:

                        options=tbloptions.objects.get(qstn=details)

                        # answer= tblans.objects.get(qstn=details)

                    except:

                        options=''

                    try:
                        answer= tblans.objects.get(qstn=details)

                    except:
                         answer=''

                        
                    dicdetails={'options':options,'question':details,'answer':answer}


                    # getdetails=getdetails.append(dicdetails)


                    return render_to_response('CBT/editqst.html',{'getdetails':dicdetails,'state':options})
                    
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                getdetails = tblcontents.objects.filter(topic=id)
                return render_to_response('lesson/entersub.html',{'gdata':getdetails})
        else:
            return HttpResponseRedirect('/login/')

def changeqst(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails = tblquestion.objects.get(id = vid)
        if request.method == 'POST':
            question = request.POST['question']
            if question == '':
                return HttpResponseRedirect ('/cbt/edit')
            getdetails.qstn = question
            getdetails.save()
            return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')

def editoptiona(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    ans= tbloptions.objects.filter(qstn=details).count()
                    if ans==0:
                        myans = tbloptioni.objects.get(qstn=details)
                    else:
                        myans = tbloptions.objects.get(qstn=details)
                    getdetails={'options':myans.a,'question':details}
                    return render_to_response('CBT/editoptiona.html',{'getdetails':getdetails})
                    
        else:
            return HttpResponseRedirect('/login/')

def optiona(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails = tblquestion.objects.get(id = vid)
        answers=tblans.objects.get(qstn=getdetails)
        boxoption = tbloptions.objects.get(qstn=getdetails)
        if request.method == 'POST':
            optiona = request.POST['optiona']
            if optiona == '':
                return HttpResponseRedirect ('/cbt/edit')

            if answers.ans == boxoption.a:
                boxoption.a = optiona,
                answers.ans = optiona
                answers.save()
                boxoption.save()
            else:
                boxoption.a = optiona
                boxoption.save()

        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')



def optionb(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails = tblquestion.objects.get(id = vid)
        answers=tblans.objects.get(qstn=getdetails)
        boxoption = tbloptions.objects.get(qstn=getdetails)
        if request.method == 'POST':
            optionb = request.POST['optionb']
            if optionb == '':
                return HttpResponseRedirect ('/cbt/edit')

            if answers.ans == boxoption.b:
                boxoption.b = optionb,
                answers.ans = optionb
                answers.save()
                boxoption.save()
            else:
                boxoption.b = optionb
                boxoption.save()

        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def optionc(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails = tblquestion.objects.get(id = vid)
        answers=tblans.objects.get(qstn=getdetails)
        boxoption = tbloptions.objects.get(qstn=getdetails)
        if request.method == 'POST':
            optionc = request.POST['optionc']
            if optionc == '':
                return HttpResponseRedirect ('/cbt/edit')

            if answers.ans == boxoption.c:
                boxoption.c = optionc,
                answers.ans = optionc
                answers.save()
                boxoption.save()
            else:
                boxoption.c = optionc
                boxoption.save()

        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')


def optiond(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails = tblquestion.objects.get(id = vid)
        answers=tblans.objects.get(qstn=getdetails)
        boxoption = tbloptions.objects.get(qstn=getdetails)
        if request.method == 'POST':
            optiond = request.POST['optiond']
            if optiond == '':
                return HttpResponseRedirect ('/cbt/edit')

            if answers.ans == boxoption.d:
                boxoption.d = optiond,
                answers.ans = optiond
                answers.save()
                boxoption.save()
            else:
                boxoption.d = optiond
                boxoption.save()

        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def chngqstimage(request,vid):
    if "userid" in request.session:
            if request.method=='POST':
                if request.FILES:
                    a=request.FILES['qstimagefile']
                    if a=='':
                        return HttpResponseRedirect('/cbt/edit/')                        
                    qst=tblquestion.objects.get(id=vid)
                    a='questions/'+str(a)
                    qst.image=a
                    qst.save()

            return HttpResponseRedirect('/cbt/edit/')
    else:
        return HttpResponseRedirect('/login/')



def editoptionb(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    ans= tbloptions.objects.filter(qstn=details).count()
                    if ans==0:
                        myans = tbloptioni.objects.get(qstn=details)
                    else:
                        myans = tbloptions.objects.get(qstn=details)
                    getdetails={'options':myans.b,'question':details}
                    return render_to_response('CBT/editoptionb.html',{'getdetails':getdetails})
                    
        else:
            return HttpResponseRedirect('/login/')


def editoptionc(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    ans= tbloptions.objects.filter(qstn=details).count()
                    if ans==0:
                        myans = tbloptioni.objects.get(qstn=details)
                    else:
                        myans = tbloptions.objects.get(qstn=details)
                    getdetails={'options':myans.c,'question':details}
                    return render_to_response('CBT/editoptionc.html',{'getdetails':getdetails})
                    
        else:
            return HttpResponseRedirect('/login/')


def editoptiond(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails=[]
                    details = tblquestion.objects.get(id = state)
                    ans= tbloptions.objects.filter(qstn=details).count()
                    if ans==0:
                        myans = tbloptioni.objects.get(qstn=details)
                    else:
                        myans = tbloptions.objects.get(qstn=details)
                    getdetails={'options':myans.d,'question':details}
                    return render_to_response('CBT/editoptiond.html',{'getdetails':getdetails})
                    
        else:
            return HttpResponseRedirect('/login/')




def myoptions(request,vid):
    if "userid" in request.session:
        varuser=request.session['userid']
        if 'option' in request.POST:
            if request.method=='POST':
                a=request.POST['optiona']
                b=request.POST['optionb']
                c=request.POST['optionc']
                d=request.POST['optiond']


                qst=tblquestion.objects.get(id=vid)
                tbloptions(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()


                gh = tbloptions.objects.get(qstn=qst)

                a = gh.a
                b = gh.b
                c= gh.c
                d= gh.d



                option = request.POST['option']
                if option=='A':
                    tblans(ans =a,option=option,qstn=qst).save()
                elif option=='B':
                    tblans(ans =b,option=option,qstn=qst).save()
                elif option=='C':
                    tblans(ans =c,option=option,qstn=qst).save()
                elif option=='D':
                    tblans(ans =d,option=option,qstn=qst).save()

                return HttpResponseRedirect('/cbt/options/')# 

            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/cbt/options/')
    else:
        return HttpResponseRedirect('/login/')


def cbtimage(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            if request.FILES:
                a=request.FILES['filetoupload']
                qt = tblquestion.objects.get(id=vid)
                qt.image=a
                qt.save()
        return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def myoptionsimage(request,vid):
    if "userid" in request.session:
            if request.method=='POST':
                if request.FILES:                
                    if 'option' in request.POST:
                        a=request.FILES['filea']
                        b=request.FILES['fileb']
                        c=request.FILES['filec']
                        d=request.FILES['filed']
                        option = request.POST['option']

                        if a=='' or b=='' or c=='' or d=='':
                            return HttpResponseRedirect('/cbt/options/')
                        
                        qst=tblquestion.objects.get(id=vid)
                        
                        tbloptioni(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()

                        gh = tbloptioni.objects.get(qstn=qst)

                        a = gh.a
                        b = gh.b
                        c= gh.c
                        d= gh.d


                        if option=='A':
                            tblans(ans =a,option=option,qstn=qst).save()
                        elif option=='B':
                            tblans(ans =b,option=option,qstn=qst).save()
                        elif option=='C':
                            tblans(ans =c,option=option,qstn=qst).save()
                        elif option=='D':
                            tblans(ans =d,option=option,qstn=qst).save()
            return HttpResponseRedirect('/cbt/options/')
    else:
        return HttpResponseRedirect('/login/')




def cbtimage(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            if request.FILES:
                a=request.FILES['filetoupload']
                qt = tblquestion.objects.get(id=vid)
                qt.image=a
                qt.save()
        return HttpResponseRedirect('/cbt/enter/question/')
    else:
        return HttpResponseRedirect('/login/')


def editquestion(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                sublist=[]
                myqst=tblquestion.objects.filter(session=session,
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam_type).order_by('klass')
                if myqst.count()==0:
                    varerr = 'NO QUESTIONS ENTERED'
                    return render_to_response('CBT/selectloan.html',{'varerr':varerr})
                else:
                    for j in myqst:    
                        k = tbloptions.objects.filter(qstn=j).count()
                        if k == 0:
                            k = tbloptioni.objects.filter(qstn=j)
                            img='hi'
                        else:
                            k = tbloptions.objects.filter(qstn=j)
                            img='low'

                        intr= {'question':j,'options':k, 'image':img}
                        sublist.append(intr)
                return render_to_response('CBT/myedit.html',{'sublist':sublist})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')



        
def options(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        form= qstnform
        qst = tblquestion.objects.all()


        # tblcomprehension.objects.all().delete()
        # tblansothers.objects.all().delete()
        # tbloptionothersi.objects.all().delete()
        # tbloptionsothers.objects.all().delete()
        # tblothers.objects.all().delete()
        # tblansblk.objects.all().delete()
        # tbloptionblki.objects.all().delete()
        # tbloptionblk.objects.all().delete()
        # tblblockquestiontblblock.objects.all().delete()
        # tblanscomp.objects.all().delete()
        # tbloptionseng.objects.all().delete()
        # tblcomprehensionqst.objects.all().delete()




        return render_to_response('CBT/options.html',{'varuser':varuser,'form':form,'qst':qst})
    else:
        return HttpResponseRedirect('/login')



def getcbtopt(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                sublist=[]


                if subject=='ENGLISH' or subject=='ENGLISH LANGUAGE':

                    return render_to_response('CBT/objeng.html',{'session':session,'term':term,'klass':klass,
                        'subject':subject,'exam':exam_type})



                    
                else:

                    myqst=tblquestion.objects.filter(session=session,
                        term=term,
                        klass=klass,
                        subject=subject,
                        exam_type=exam_type)

                    if myqst.count()==0:
                        varerr = 'NO QUESTIONS ENTERED'
                        return render_to_response('CBT/selectloan.html',{'varerr':varerr})


                    else:
                        for j in myqst:

                            try:
                                ans = tblans.objects.get(qstn = j).option
                            except:
                                ans= ''
                            k = tbloptions.objects.filter(qstn=j).count()
                            if k == 0:
                                k = tbloptioni.objects.filter(qstn=j)
                                img='hi'
                            else:
                                k = tbloptions.objects.filter(qstn=j)
                                img='low'

                            intr= {'question':j,'options':k, 'image':img,'ans':ans}
                            sublist.append(intr)
                        return render_to_response('CBT/myopt.html',{'sublist':sublist,})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
        


def getcbtengedit(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                sublist=[]


                if subject=='ENGLISH' or subject=='ENGLISH LANGUAGE':

                    return render_to_response('CBT/objeditng.html',{'session':session,'term':term,'klass':klass,
                        'subject':subject,'exam':exam_type})


                    
                else:

                    myqst=tblquestion.objects.filter(session=session,
                        term=term,
                        klass=klass,
                        subject=subject,
                        exam_type=exam_type)

                    if myqst.count()==0:
                        varerr = 'NO QUESTIONS ENTERED'
                        return render_to_response('CBT/selectloan.html',{'varerr':varerr})


                    else:
                        for j in myqst:

                            try:
                                ans = tblans.objects.get(qstn = j).option
                            except:
                                ans= ''

                            k = tbloptions.objects.filter(qstn=j).count()
                            if k == 0:
                                k = tbloptioni.objects.filter(qstn=j)
                                img='hi'
                            else:
                                k = tbloptions.objects.filter(qstn=j)
                                img='low'

                            intr= {'question':j,'options':k, 'image':img, 'ans':ans}
                            sublist.append(intr)
                        return render_to_response('CBT/myoptedit.html',{'sublist':sublist,})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')




def editq(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        form= qstnform
        qst = tblquestion.objects.all()
        return render_to_response('CBT/edit.html',{'varuser':varuser,'form':form,'qst':qst})
    else:
        return HttpResponseRedirect('/login')




def getcats(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
                session,term,klass,subject,exam_type,category= acccode.split(':')
                # sublist=[]

                if category=='-----':
                    msg='Select a category'                    
                    return render_to_response('CBT/selectloan.html',{'msg':msg})
                
                elif category== 'Comprension':

                    allq=[]

                    try:
                        comp=tblcomprehension.objects.get(session=session,                        
                            term=term,
                            klass=klass,
                            subject=subject,
                            exam_type=exam_type)

                    except :
                        msg = 'No questions found'
                        return render_to_response('CBT/selectloan.html',{'msg':msg})
                        

                    questions=tblcomprehensionqst.objects.filter(comprehension = comp)



                    for pk in questions:
                        try:
                            fo=tbloptionseng.objects.get(qstn=pk)
                            ans = tblanscomp.objects.get(qstn=pk).option
                        
                        except:
                            fo = 'No options yet'
                            ans='No ans yet'

                        hg= {'ques':pk,'opt':fo,'vid':pk.qstcode,'ans':ans}
                        allq.append(hg)

                                

                    return render_to_response('CBT/objoption.html',{'quest':allq,'term':term,  
                        'subject':subject,   
                        'exam':exam_type,   
                        'comp':comp, 
                        'klass':klass, 
                        'session':session})

                
                elif category == 'Block':
                    try:
                        blk=tblblock.objects.filter(session=currse,
                            term=term,
                            klass=klass,
                            exam_type=exam_type,
                            subject=subject)

                        allqst=[]

                        for k in blk:
                            qst = tblblockquestion.objects.filter(block=k)

                            for qqq in qst:
                                pl = tbloptionblki.objects.filter(qstn=qqq)
                                kp=pl.count()
                                if kp == 0:                         
                                    opt = tbloptionblk.objects.filter(qstn=qqq)
                                    msg='txt'                     
                                else:
                                    opt = pl
                                    msg='img'


                                try:
                                    ans = tblansblk.objects.get(qstn=qqq).option
                                except:
                                    ans='No ans yet'


                                lk={'qst':qqq,'opt':opt,'msg':msg,'ans':ans}
                                allqst.append(lk)
                            


                        return render_to_response('CBT/blkopt.html',{'q':allqst,
                            'term':term,
                            'inst':blk,
                            'subject':subject,
                            'Exam':exam_type,
                            'klass':klass,
                            'session':session})

                    except:
                        msg ='No block questions found'
                        return render_to_response('CBT/selectloan.html',{'msg':msg})
                
                elif category == 'Others':

                    try:

                        qqq=tblothers.objects.filter(session=session,                        
                            term=term,
                            klass=klass,
                            subject=subject,
                            exam_type=exam_type)


                        qt=[]

                        for n in qqq:
                            opt =tbloptionothersi.objects.filter(qstn =n)
                            msg = 'img'
                            fv= opt.count()
                            if fv ==0:
                                opt = tbloptionsothers.objects.filter(qstn=n)
                                msg = 'txt'
                                fv =1

                            if fv == 1:
                                try:
                                    ans = tblansothers.objects.get(qstn=n).option
                                except:
                                    ans='No ans yet'
      
                            tr = {'question':n, 'options':opt,'id':n.id,'msg':msg,'ans':ans}
                            qt.append(tr)


                        return render_to_response('CBT/othersopt.html',{'qq':qt,'term':term,
                            'subject':subject,
                            'others':qqq,
                            'exam':exam_type,
                            'klass':klass,'session':session})
                        
                    except:
                        msg = 'No questions found '
                        return render_to_response('CBT/selectloan.html',{'msg':msg})


            else:
                return HttpResponseRedirect('/welcome/')


    else:
        return HttpResponseRedirect('/login/')









def editallentry(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state=acccode
                session,term,klass,subject,exam_type,category= acccode.split(':')
                # sublist=[]

                if category=='-----':
                    msg='Select a category'                    
                    return render_to_response('CBT/selectloan.html',{'msg':msg})
                
                elif category== 'Comprension':

                    allq=[]

                    try:
                        comp=tblcomprehension.objects.get(session=session,                        
                            term=term,
                            klass=klass,
                            subject=subject,
                            exam_type=exam_type)

                    except :
                        msg = 'No questions found'
                        return render_to_response('CBT/selectloan.html',{'msg':msg})
                        

                    questions=tblcomprehensionqst.objects.filter(comprehension = comp)



                    for pk in questions:
                        try:
                            fo=tbloptionseng.objects.get(qstn=pk)
                            ans = tblanscomp.objects.get(qstn=pk).option
                        
                        except:
                            fo = 'No options yet'
                            ans='No ans yet'

                        hg= {'ques':pk,'opt':fo,'vid':pk.qstcode,'ans':ans}
                        allq.append(hg)
                                

                    return render_to_response('CBT/compedit.html',{'quest':allq,'term':term,  
                        'subject':subject,   
                        'exam':exam_type,   
                        'comp':comp, 
                        'klass':klass, 
                        'session':session})

                
                elif category == 'Block':
                    try:
                        blk=tblblock.objects.filter(session=currse,
                            term=term,
                            klass=klass,
                            exam_type=exam_type,
                            subject=subject)

                        allqst=[]

                        for k in blk:
                            qst = tblblockquestion.objects.filter(block=k)

                            for qqq in qst:
                                pl = tbloptionblki.objects.filter(qstn=qqq)
                                kp=pl.count()
                                if kp == 0:                         
                                    opt = tbloptionblk.objects.filter(qstn=qqq)
                                    msg='txt'                     
                                else:
                                    opt = pl
                                    msg='img'


                                try:
                                    ans = tblansblk.objects.get(qstn=qqq).option
                                except:
                                    ans='No ans yet'


                                lk={'qst':qqq,'opt':opt,'msg':msg,'ans':ans}
                                allqst.append(lk)
                            


                        return render_to_response('CBT/blkedit.html',{'q':allqst,
                            'term':term,
                            'inst':blk,
                            'subject':subject,
                            'Exam':exam_type,
                            'klass':klass,
                            'session':session})

                    except:
                        msg ='No block questions found'
                        return render_to_response('CBT/selectloan.html',{'msg':msg})
                
                elif category == 'Others':

                    try:

                        qqq=tblothers.objects.filter(session=session,                        
                            term=term,
                            klass=klass,
                            subject=subject,
                            exam_type=exam_type)


                        qt=[]

                        for n in qqq:
                            opt =tbloptionothersi.objects.filter(qstn =n)
                            msg = 'img'
                            fv= opt.count()
                            if fv ==0:
                                opt = tbloptionsothers.objects.filter(qstn=n)
                                msg = 'txt'
                                fv =1

                            if fv == 1:
                                try:
                                    ans = tblansothers.objects.get(qstn=n).option
                                except:
                                    ans='No ans yet'
      
                            tr = {'question':n, 'options':opt,'id':n.id,'msg':msg,'ans':ans}
                            qt.append(tr)


                        return render_to_response('CBT/othersedit.html',{'qq':qt,'term':term,
                            'subject':subject,
                            'others':qqq,
                            'exam':exam_type,
                            'klass':klass,'session':session})
                        
                    except:
                        msg = 'No questions found '
                        return render_to_response('CBT/selectloan.html',{'msg':msg})


            else:
                return HttpResponseRedirect('/welcome/')


    else:
        return HttpResponseRedirect('/login/')


def otheroption(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                details = tblothers.objects.get(qstcode = state)

                try:
                    options= tbloptionothersi.objects.get(qstn=details)
                    answer= tblansothers.objects.get(qstn=details)
                    dicdetails={'options':options,'question':details,'answer':answer}                    
                    return render_to_response('CBT/othersimage.html',{'getdetails':dicdetails})

                except:

                    opt= tbloptionsothers.objects.filter(qstn=details)
                    if opt.count()>0:
                        options= tbloptionsothers.objects.get(qstn=details)
                        answer= tblansothers.objects.get(qstn=details)
                        dicdetails={'options':options,'question':details,'answer':answer}                    
                        return render_to_response('CBT/otherqstpop.html',{'getdetails':dicdetails})

                    else:
                        return render_to_response('CBT/chooseothers.html',{'state':state})

    else:
        return HttpResponseRedirect('/login/')



def othertextts(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblothers.objects.get(qstcode=vid)
            session=qst.session
            subject=qst.subject
            term=qst.term
            exam=qst.exam_type
            code=qst.qstcode

            return HttpResponseRedirect('/cbt/input_text/otherssqst/%s/%s/%s/%s/'%(code,
                str(session).replace('/','k'),
                term,  str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')


def save_othertext(request,code,session,term,exam):
    session = str(session).replace('k','/')
    term = str(term).replace('w',' ')
    exam = str(exam).replace('p',' ')



    if request.method == 'GET':
        getdetails=[]
        details = tblothers.objects.get(qstcode = code)
            
        dicdetails={'question':details}

        return render_to_response('CBT/enterothropt.html',{'getdetails':dicdetails})


def save_othermages(request,code,session, term,subject,exam):
    session = str(session).replace('k','/')
    subject = str(subject).replace('w',' ')
    exam = str(exam).replace('p',' ')

    if request.method == 'GET':
        getdetails=[]
        details = tblothers.objects.get(qstcode = code)
            
        dicdetails={'question':details}

        return render_to_response('CBT/otherqstimage.html',{'getdetails':dicdetails})


def myotheroptions(request,vid):
    if "userid" in request.session:
        varuser=request.session['userid']

        if 'option' in request.POST:
            if request.method=='POST':
                a=request.POST['optiona']
                b=request.POST['optionb']
                c=request.POST['optionc']
                d=request.POST['optiond']



                qst=tblothers.objects.get(qstcode=vid)
                tbloptionsothers(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()
                
                gh = tbloptionsothers.objects.get(qstn=qst)

                a = gh.a
                b = gh.b
                c= gh.c
                d= gh.d


                option = request.POST['option']
                if option=='A':
                    tblansothers (ans =a,option=option,qstn=qst).save()
                elif option=='B':
                    tblansothers(ans =b,option=option,qstn=qst).save()
                elif option=='C':
                    tblansothers(ans =c,option=option,qstn=qst).save()
                elif option=='D':
                    tblansothers(ans =d,option=option,qstn=qst).save()
                g= 'my name is mathew'
                return HttpResponseRedirect('/cbt/options/')# 

            else:
                return HttpResponseRedirect('/login/')
        else:
            f = 'my name is black'
            return HttpResponseRedirect('/cbt/options/')
    else:
        return HttpResponseRedirect('/login/')





def entcompopt(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                details = tblcomprehensionqst.objects.get(qstcode = state)


                try:
                    options= tbloptionseng.objects.get(qstn=details)
                    answer= tblanscomp.objects.get(qstn=details)
                    dicdetails={'options':options,'question':details,'answer':answer}

                    return render_to_response('CBT/viewengcomp.html',{'getdetails':dicdetails
                        
                        })

                except:
             
                    return render_to_response('CBT/popcomp.html',{'getdetails':details})#},'session':session})

    else:
        return HttpResponseRedirect('/login/')


def entercompoptions(request,vid):
    if "userid" in request.session:
        varuser=request.session['userid']
        # session = request.session['session']

        if 'option' in request.POST:
            if request.method=='POST':
                a=request.POST['optiona']
                b=request.POST['optionb']
                c=request.POST['optionc']
                d=request.POST['optiond']







                qst=tblcomprehensionqst.objects.get(qstcode=vid)

                tbloptionseng(a=a,b=b,c=c,d=d,e='non of the above',qstn=qst).save()
              
                gh =  tbloptionseng.objects.get(qstn=qst)

                a = gh.a
                b = gh.b
                c= gh.c
                d= gh.d


                option = request.POST['option']

                if option=='A':
                    tblanscomp(ans =a,option=option,qstn=qst).save()
                elif option=='B':
                    tblanscomp(ans =b,option=option,qstn=qst).save()
                elif option=='C':
                    tblanscomp(ans =c,option=option,qstn=qst).save()
                elif option=='D':
                    tblanscomp(ans =d,option=option,qstn=qst).save()

                return HttpResponseRedirect('/cbt/options/') 

            else:
                return HttpResponseRedirect('/login/')
        else:

            return HttpResponseRedirect('/cbt/options/') 

    else:
        return HttpResponseRedirect('/login/')




def edtcompqst(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    return render_to_response('CBT/edcompqst.html',{'q':details})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')



def edtoptt(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state,option=acccode.split(':')
            

                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    optionA=tbloptionseng.objects.get(qstn=details).a

                    return render_to_response('CBT/edoptqst.html',{'a':optionA,'opt':option,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')



def editoptioA(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']


            old_optionA = request.POST['getdetails']

            details = tblcomprehensionqst.objects.get(qstcode = vid)


            
            options=tbloptionseng.objects.get(qstn=details)

            ans2 = tblanscomp.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.a =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.a =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')







def edtopttb(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state,option=acccode.split(':')
            

                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    optionA=tbloptionseng.objects.get(qstn=details).b

                    return render_to_response('CBT/edoptqstB.html',{'a':optionA,'opt':option,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')



def editoptioB(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']

            old_optionA = request.POST['getdetails']

            details = tblcomprehensionqst.objects.get(qstcode = vid)


            
            options=tbloptionseng.objects.get(qstn=details)

            ans2 = tblanscomp.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.b =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.b =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def edtopttc(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state,option=acccode.split(':')
            

                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    optionA=tbloptionseng.objects.get(qstn=details).c

                    return render_to_response('CBT/edoptqstC.html',{'a':optionA,'opt':option,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')



def editoptioC(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']

            old_optionA = request.POST['getdetails']

            details = tblcomprehensionqst.objects.get(qstcode = vid)


            
            options=tbloptionseng.objects.get(qstn=details)

            ans2 = tblanscomp.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.c =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.c =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def edtopttd(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state,option=acccode.split(':')
            

                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    optionA=tbloptionseng.objects.get(qstn=details).d

                    return render_to_response('CBT/edoptqstD.html',{'a':optionA,'opt':option,'code':state})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')



def editoptioD(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            optionA = request.POST['optionA']

            old_optionA = request.POST['getdetails']

            details = tblcomprehensionqst.objects.get(qstcode = vid)


            
            options=tbloptionseng.objects.get(qstn=details)

            ans2 = tblanscomp.objects.get(qstn=details)
            ans = ans2.ans

            if optionA == ans:
                options.d =old_optionA
                options.save()


                ans2.ans=old_optionA
                ans2.save()


            else:
                options.d =old_optionA
                options.save()

            return HttpResponseRedirect('/cbt/edit/')



        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')




def edtans(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
            
                getdetails=[]
                try:
                    details = tblcomprehensionqst.objects.get(qstcode = state)
                    options=tbloptionseng.objects.get(qstn=details)
                    ans=tblanscomp.objects.get(qstn=details)

                    return render_to_response('CBT/aditcompans.html',{'ans':ans,'qst':details,'opt':options})

                except:
                    msg = 'no AVAILABLE'
                return render_to_response('CBT/selectloan.html',{'msg':msg})


    else:
        return HttpResponseRedirect('/login/')

def changeansw(request,vid):

    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]


            if 'gender' in request.POST:
                answer = request.POST['gender']
                details = tblcomprehensionqst.objects.get(qstcode=vid)
                ans=tblanscomp.objects.get(qstn=details)
                options=tbloptionseng.objects.get(qstn=details)

                if answer == options.a:
                    ppp = 'A'
                if answer == options.b:
                    ppp = 'B'

                if answer == options.c:
                    ppp = 'C'

                if answer == options.d:
                    ppp = 'D'



                ans.ans = answer
                ans.option=ppp
                ans.save()


        return HttpResponseRedirect('/cbt/edit/')

    else:
        return HttpResponseRedirect('/login/')




def theory(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        if request.method=='POST':
            form = theoryform(request.POST, request.FILES)

            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                klass=form.cleaned_data['klass']
                exam_type=form.cleaned_data['exam_type']
                subject=form.cleaned_data['subject']
                rfile=form.cleaned_data['pix']

                if rfile is None:
                    pix = '/ax/image'
                    msg='sdff'
                else:
                    pix = request.FILES['pix']
                    msg =' na we be this'

                tbltheory(session=session,
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam_type,
                    image=pix).save()

                msg =' image saved successfully'                
                    
                return render_to_response('CBT/selectloan.html',{'msg':msg})
                # return HttpResponseRedirect('/cbt/enter/theory/')
            else:
                return HttpResponseRedirect('/welcome/')


        else:
            form = theoryform()
            return render_to_response('CBT/theory.html',{'varuser':varuser,'form':form})

    else:
        return HttpResponseRedirect('/login/')



def gettheoryajax(request):
    if  "userid" in request.session:
        if request.is_ajax():

            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,exam,term, subject= acccode.split(':')
                th=tbltheory.objects.filter(exam_type=exam, session=session,term=term,klass=klass,subject=subject)
                # return HttpResponse(json.dumps(kk), mimetype='application/json')
                return render_to_response('CBT/theoajax.html',{'data':th})

    else:
        return HttpResponseRedirect('/login/')


def deltheory(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode        
                # getdetails=[]
                try:
                    details = tbltheory.objects.get(id = state)       
                    return render_to_response('CBT/delthe.html',{'data':details})
                except:
                    return HttpResponseRedirect('/cbt/enter/theory/')
        
        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def theorydelete(request,vid):
    if  "userid" in request.session:
        if request.method == 'POST':
            details = tbltheory.objects.get(id = vid)
            details.delete()
            return HttpResponseRedirect('/cbt/enter/theory/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def markguide(request):
    if "userid" in request.session:
        varuser=request.session['userid']
        form= qstnform
        qst = tblquestion.objects.all()
        return render_to_response('CBT/markguide.html',{'varuser':varuser,'form':form,'qst':qst})
    else:
        return HttpResponseRedirect('/login')




def pupilcbt(request): #the start buttin
    if "userid" in request.session:
        
        if request.method=='POST':
            varuser=request.session['userid']
            ex=tblcbtexams.objects.get(status='ACTIVE')

            student=Student.objects.get(admitted_session=currse,
                admissionno=varuser,
                gone=False)

            now_scheduled= scheduled.objects.get(student=student,
                term=term,
                assessment=ex.exam_type,
                session=currse)

            subject=now_scheduled.subject


            qstns=tblquestion.objects.filter(term=term,
                exam_type=ex.exam_type,
                session=currse,
                subject=subject,
                klass=student.admitted_class)

            qcount=qstns.count()

            try: #student already started ut logged out

                fq=cbtcurrentquestion.objects.get(student=student,
                session=currse,
                term=term,
                subject=subject,
                exam_type=ex.exam_type)
                

                number=int(fq.number)
                
                try: #if its an already answered question
                    mqst =cbttrans.objects.get(student=student,session=currse,
                        term=term,
                        exam_type=ex.exam_type,
                        subject=subject,
                        no=number)

                    ans=mqst.stu_ans

                    tk =qstns.get(id=mqst.qstcode)

                    tk1 =tk.qstn
                    img=tk.image

                    k = tbloptions.objects.filter(qstn=tk).count()
                    if k == 0:
                        opt = tbloptioni.objects.filter(qstn=tk)
                        image='hi'
                    else:
                        opt = tbloptions.objects.filter(qstn=tk)
                        image='low'
                    
                    uid= tk.id

                    return render_to_response('CBT/previous.html',{'question':tk1,
                        'school':school,
                        'count':number,
                        'pos':image,
                        'ans':ans,
                        'image':img,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'uid':tk.id,
                        'subject':subject})

                except: #if its a fresh question

                    mqst =cbtold.objects.get(student=student,session=currse,
                        term=term,
                        exam_type=ex.exam_type,
                        subject=subject,
                        klass=student.admitted_class)

                    ans=''

                    tk =qstns.get(id=mqst.qstcode)

                    tk1 =tk.qstn
                    img=tk.image

                    k = tbloptions.objects.filter(qstn=tk).count()
                    if k == 0:
                        opt = tbloptioni.objects.filter(qstn=tk)
                        image='hi'
                    else:
                        opt = tbloptions.objects.filter(qstn=tk)
                        image='low'
                    
                    uid= tk.id
                    

            except:#student just starting the paper or i am done

##COLLECTING ANSWERED QUESTIONS BY ID
                trans=cbttrans.objects.filter(session=currse,
                    exam_type=ex.exam_type,
                    student=student,
                    subject=subject,
                    term=term)

                nu = trans.count()

                transid=[int(k.qstcode) for k in trans]

##COLLECTING ENTERED QUESTIONS BY ID

                myq=[q.id for q in qstns]               
       

##SORTING OUT UNIQUE QUESTIONS
                qu=[]
                qu= [item for item in myq  if item not in transid]


                if qu == []:

                    return render_to_response('CBT/done.html')


##PICKING A RANDOM UNIQUE QUESTION BY ID
                uid = 0
                uid = random.choice(qu)
                tk=0
                
                tk = qstns.get(id=uid)

                try:
                    cbtold.objects.get(session=currse,
                    question=tk,
                    term=q.term,
                    exam_type=q.exam_type,
                    klass=student.admitted_class,
                    subject=subject,
                    student=student,
                    qstcode=tk.id)

                except:
                    cbtold(session=currse,
                    question=tk,
                    term=q.term,
                    exam_type=q.exam_type,
                    klass=student.admitted_class,
                    subject=subject,
                    student=student,
                    qstcode=tk.id).save()       

                tk1 =tk.qstn

                k = tbloptions.objects.filter(qstn=tk).count()
                if k == 0:
                    opt = tbloptioni.objects.filter(qstn=tk)
                    image='hi'
                else:
                    opt = tbloptions.objects.filter(qstn=tk)
                    image='low'


                img=tk.image
                ans=''

                number=nu + 1

                try:
                    cbtcurrentquestion.objects.get(student=student,
                    term = term,
                    session=currse,
                    subject=subject,
                    exam_type=ex.exam_type,
                    number=number)

                except:
                    cbtcurrentquestion(student=student,
                        term = term,
                        session=currse,
                        subject=subject,
                        exam_type=ex.exam_type,
                        number=number).save()
                    
                    number=number

            return render_to_response('CBT/pupiltest.html',{'varuser':varuser, 'question':tk1,
                'school':school,
                'count':number,
                'image':img,
                'pos':image,
                'ans':ans,
                'questioncount':qcount,
                'form':student,
                'session':currse,
                'name':student.admissionno,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'uid':uid,
                'subject':subject})

        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')






def pushstart(request): #the start buttin
    if "userid" in request.session:






        kln = 'yes'

        if kln == 'yes':

            
            df = tblcbtcurrentquestioneng.objects.all()
            df.delete()
            
            vv = tblcbtoldeng.objects.all()
            vv.delete()

            fv = tblcbttranscomp.objects.all()
            fv.delete()


            current_time= datetime.time(datetime.now()) #extract current time from datetime

            t= tblcbtsubject.objects.get(subject='ENGLISH',klass= 'JS 1')
            t.st_time = current_time
            t.save()

        


        if request.method=='POST':
            varuser=request.session['userid']

            ex=tblcbtexams.objects.get(status='ACTIVE')

            student=Student.objects.get(admitted_session=currse,
                admissionno=varuser,
                gone=False)

            klass=student.admitted_class

            now_scheduled= scheduled.objects.get(student=student,
                term=term,
                assessment=ex.exam_type,
                session=currse)



            subject=now_scheduled.subject

            mbg  = questioncount(currse,klass,term,subject,ex.exam_type)



            disp_no = tblcbtcurrentquestioneng.objects.filter(session=currse,
                term=term,
                subject=subject,
                student=student, 
                exam_type=ex.exam_type)

            disp_no_count = disp_no.count()


            t= tblcbtsubject.objects.get(subject=subject,
                klass= student.admitted_class,
                session=currse,
                term=term,exam_type=ex.exam_type)
            duration=t.duration

            try:
                timestamp = cbttimestable.objects.get(student=student,subject=subject,term=term,exam_type=ex.exam_type)
            except:
                cbttimestable(student=student,subject=subject,start_time=ttimee ,duration =duration, term=term,exam_type=ex.exam_type).save()

            

            if disp_no_count ==1: #there was a displayed question

                cvcc = current_question(currse,term,subject,student,ex.exam_type)
                n2 = cvcc['number']


                disp_no= disp_no.get()

                disp_no_number = disp_no.number
                # n2 = disp_no_number

                disp_qst = tblcbtoldeng.objects.get(question=disp_no, qstno=n2)

                disp_qst_category  = disp_qst.category
                disp_qst_code = disp_qst.qstcode


                #chk if its an allready answered question
                my_comp_qst= tblcbttranscomp.objects.filter(qstcode=disp_qst.qstcode,student=student)

                if my_comp_qst.count() == 1: #Stale question                                   

                    pik = tblcbttranscomp.objects.get(student=student,session=currse,
                        term=term, exam_type=ex.exam_type,qno=n2,subject=subject)
                                   
                    ans=pik.stu_ans
                    category=pik.category
                    qstcode=pik.qstcode
                    groupcode=pik.groupcode

                    cvcc['asd'].number = n2
                    cvcc['asd'].save()              

                    tblcbtoldeng.objects.filter(question=cvcc['asd']).update(qstno=n2, qstcode=qstcode,groupcode=groupcode,category=category)

                    dis = display_answered_qstn(qstcode,category,n2)


                    if category=='C': #stale and  comprehension
                        return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':dis['question'],
                            'school':school,
                            'qq':dis['qq'],
                            'image':dis['image'],
                            'options':dis['options'],
                            'pos':dis['pos'],
                            'ans':ans,
                            'total':mbg,
                            'exam': ex.exam_type,

                            'groupcode':'fu',
                            'code':dis['question'].qstcode,

                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'term':term,
                            'subject':subject})


                    elif category == 'block':#stale and block
                    
                        return render_to_response('CBT/blkprevious.html',{'varuser':varuser, 'question':dis['question'],
                             'school':school,
                            'qq':dis['qq'],
                            'options':dis['options'],
                            'total':mbg,
                            'ans':ans,
                            'groupcode':dis['question'].block.code,
                            'code':dis['question'].qstcode,
                            'pos':dis['pos'],
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'term':term,
                            'subject':subject})



                    elif category == 'others':#stale and others
                        return render_to_response('CBT/othersprev.html',{'varuser':varuser, 'question':dis['question'],
                            'school':school,
                            'qq':dis['qq'],
                            'image':dis['image'],
                            'options':dis['options'],
                            'ans':ans,
                            'total':mbg,
                            'pos':dis['pos'],
                            'groupcode': groupcode,
                            'code':qstcode,
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':klass,
                            'adm':student.admissionno,                            
                            'term':term,
                            'subject':subject})


                elif my_comp_qst.count() == 0: #fresh question


                    if disp_qst_category=='C': #fresh and comprehension                               

                        ccp_code = retrieve_comprehension_question_detail(disp_qst_code,student)
                        myq = ccp_code['question']

        

                        ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                        next_no = ft - ccp_code['solved'] + 1
                        qq=  ft  + 1

                        to = ft + ccp_code['remain']


                        opt = tbloptionseng.objects.get(qstn = myq)
                        
                        uid= disp_no_number
                        number= disp_no_number
                        image= myq.comprehension.qstimage
                        pos='pos'                        
                        img='img'

                        # msg ='i am left'   return render_to_response('CBT/selectloan.html',{'msg':msg})

                        return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                            'school':school,
                            'count':next_no,
                            'to': to,
                            'qq':qq,
                            'total':mbg,
                            'groupcode':'fu',
                            'code':ccp_code['question'].qstcode,
                            'exam':ex.exam_type,
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'options':opt,
                            'term':term,
                            'subject':subject})


                    elif disp_qst_category=='block':#fresh and block 

                        ccp_code = retrieve_question_detailblk(disp_qst_code,student)
                        

                        myq = ccp_code['question']
                        groupcode = ccp_code['question'].block.code
                       

                        try :
                            opt = tbloptionblk.objects.get(qstn=myq)
                            pos = 'low'
                        except:
                            opt = tbloptionblki.objects.get(qstn = myq)
                            pos = 'hi'

                        ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                        next_no = ft - ccp_code['solved'] + 1
                        qq=  ft  + 1

                        to = ft + ccp_code['remain']
            

                        return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                            'school':school,
                            'count':next_no,
                            'qq':qq,
                            'to': to,
                            'total':mbg,
                            'pos':pos,
                            'groupcode':groupcode,
                            'code':ccp_code['question'].qstcode,
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'options':opt,
                            'term':term,
                            'subject':subject})


                    elif disp_qst_category == 'others':#fresh and others

                       
                        myq = tblothers.objects.get(qstcode=disp_qst_code)

                        try :
                            opt = tbloptionsothers.objects.get(qstn=myq)
                            pos = 'low'
                        except:
                            opt = tbloptionothersi.objects.get(qstn = myq)
                            pos = 'hi'

                        ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                        next_no = ft  + 1
                        qq=  ft  + 1

                        to = ft #+ ccp_code['remain']
                       


                        return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'to': to,
                                'qq':qq,
                                'total':mbg,
                                'pos':pos,
                                'groupcode':'AA',
                                'code':disp_qst_code,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})


            elif disp_no_count == 0: #There was no displayed qustion                               

                dnsc= tblcbttranscomp.objects.filter(session=currse,category='C',
                    exam_type=ex.exam_type,student=student,subject=subject,term=term)


                ghccp = [str(s.qstcode) for s in dnsc]


                comp = tblcomprehension.objects.get(session=currse,
                    term =term,
                    klass=klass,
                    subject=subject,
                    exam_type=ex.exam_type)

                comp_qst = tblcomprehensionqst.objects.filter(comprehension=comp) 
                ccp = [str(s.qstcode) for s in comp_qst] #all comp questions


                ghy= [k for k in ccp if k not in ghccp] #unanswrd compr qstns


                if len(ghy)> 0: #
                    tt = random.choice(ghy)
                    ccp_code = retrieve_comprehension_question_detail(tt,student)

                    myq = ccp_code['question']


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                    next_no = ft - ccp_code['solved'] +1

                    qq=  ft  + 1

                    number = ft +1

                    to = ft + ccp_code['remain']



                    opt = tbloptionseng.objects.get(qstn = myq)



                    try:
                        sst = tblcbtcurrentquestioneng.objects.get(session=currse, 
                            term=term,
                            exam_type=ex.exam_type,
                            subject=subject,
                            student=student)
                    except:

                        tblcbtcurrentquestioneng(session=currse,
                            term=term,
                            exam_type=ex.exam_type,
                            subject=subject,
                            student=student,
                            number=number).save()

                        sst = tblcbtcurrentquestioneng.objects.get(session=currse, term=term, 
                            exam_type=ex.exam_type, subject=subject,student=student)



                    tblcbtoldeng(question=sst,
                        qstcode=ccp_code['question'].qstcode,
                        qstno=number, category='C',groupcode='fu').save()

                    

                    image =myq.comprehension.qstimage



                    return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'to': to,
                        'qq':qq,
                        'total':mbg,
                        'groupcode':'fu',
                        'code':ccp_code['question'].qstcode,
                        'form':student,
                        'exam':ex.exam_type,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})

                else:
                    blk = tblblock.objects.filter(session=currse,term=term, 
                        klass=klass, exam_type=ex.exam_type,subject=subject)

                    instruction_code =[str(k.code) for k in blk]

                    if len(instruction_code) > 0:

                        # ttt = total_ans_qst(currse,term,subject,ex.exam_type)
                        ttt = total_ans_qst(currse,term,subject,student,ex.exam_type)  #total answered question all together

                        for k in instruction_code:
                            myblk = blk.get(code = k)
                            qst = tblblockquestion.objects.filter(block = myblk)
                            qst_count = qst.count() #total number of blk question

                            qst_code = [str(d.qstcode) for d in qst]


                            done_blk_qst = tblcbttranscomp.objects.filter(session=currse,
                                term=term,subject=subject,exam_type=ex.exam_type,student=student,
                                groupcode=k,category='blk') #total number of answered question

                            done_blk_qst_count=done_blk_qst.count()

                            undone = int(qst_count) - int(done_blk_qst_count)

                            t_undone = ttt + undone

                            done_code = [str(d.qstcode) for d in done_blk_qst]

                            unk_qst = [j for j in qst_code if j not in done_code]

                            if len(unk_qst)> 0:
                                ccp_code = random.choice(unk_qst)
                                myq = qst.get(qstcode=ccp_code)

                                try:
                                    opt = tbloptionblki.objects.get(qstn=myq)
                                except:
                                    opt = tbloptionblk.objects.get(qstn=myq)


                                ans = tblansblk.objects.get(qstn=myq)

                                uid=0



                                return render_to_response('CBT/blkprevious.html',{'varuser':varuser, 'question':myq,
                                    'school':school,
                                    'count':ttt+1,
                                    # 'ans':ans,
                                    'questioncount':t_undone,
                                    'form':student,
                                    'instr':myblk,
                                    'session':currse,
                                    'name':student.admissionno,
                                    'klass':student.admitted_class,
                                    'adm':student.admissionno,
                                    'options':opt,
                                    'term':term,
                                    'uid':uid,
                                    'subject':c})                        

                    else:

                        msg = 'im done with block'
                        return render_to_response('CBT/selectloan.html',{'msg':msg})



            else:
                return HttpResponseRedirect('/welcome/')

        else:
            return HttpResponseRedirect('/welcome/')

    else:
        return HttpResponseRedirect('/login/')





def nabefore(request):
    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]

            code2 = request.POST['code']

            groupcode2 = request.POST['groupcode']

            student= Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)
            klass=student.admitted_class 
            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)
            subject=now_scheduled.subject

            
            cvcc = current_question(currse,term,subject,student,ex.exam_type)

            mbg  = questioncount(currse,klass,term,subject,ex.exam_type)

            # msg = cvcc['asd'].number, cvcc['number']   return render_to_response('CBT/selectloan.html',{'msg':msg})
            
            if cvcc['code']==code2 :

                if int(cvcc['asd'].number)==1:
                    # msg = cvcc['asd'].number, cvcc['number']          
                    # return render_to_response('CBT/selectloan.html',{'msg':msg})


                    pik = tblcbttranscomp.objects.filter(student=student,session=currse,
                        term=term, exam_type=ex.exam_type,qno=1,subject=subject)

                    if pik.count() == 1:
                        pik = pik.get()
                        ans=pik.stu_ans
                        category=pik.category
                        qstcode=pik.qstcode
                        groupcode=pik.groupcode
                        dis = display_answered_qstn(qstcode,category,1)

                        return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':dis['question'],
                            'school':school,
                            'qq':dis['qq'],
                            'image':dis['image'],
                            'options':dis['options'],
                            'pos':dis['pos'],
                            'ans':ans,
                            'total':mbg,
                            'groupcode':'fu',
                            'code':dis['question'].qstcode,
                            'exam': ex.exam_type,
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'term':term,
                            'subject':subject})


                    else:
                        dis = display_answered_qstn(cvcc['code'],cvcc['category'],cvcc['number'])

                        return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':dis['question'],
                            'school':school,
                            'qq':dis['qq'],
                            'image':dis['image'],
                            'options':dis['options'],
                            'pos':dis['pos'],
                            'total':mbg,
                            'groupcode':'fu',
                            'code':dis['question'].qstcode,
                            'exam':ex.exam_type,
                            'form':student,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'term':term,
                            'subject':subject})

                else:
                    n2=int(cvcc['number']) - 1

                pik = tblcbttranscomp.objects.get(student=student,session=currse,
                    term=term, exam_type=ex.exam_type,qno=n2,subject=subject)
                               
                ans=pik.stu_ans
                category=pik.category
                qstcode=pik.qstcode
                groupcode=pik.groupcode

                cvcc['asd'].number = n2
                cvcc['asd'].save()              

                tblcbtoldeng.objects.filter(question=cvcc['asd']).update(qstno=n2, qstcode=qstcode,groupcode=groupcode,category=category)

                dis = display_answered_qstn(qstcode,category,n2)

                if category =='C':              

                    return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':dis['question'],
                        'school':school,
                        'qq':dis['qq'],
                        'image':dis['image'],
                        'options':dis['options'],
                        'pos':dis['pos'],
                        'ans':ans,
                        'total':mbg,
                        'groupcode':'fu',
                        'code':dis['question'].qstcode,
                        'exam': ex.exam_type,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'term':term,
                        'subject':subject})


                elif category=='block':
                
                    return render_to_response('CBT/blkprevious.html',{'varuser':varuser, 'question':dis['question'],
                        'school':school,
                        'qq':dis['qq'],
                        'options':dis['options'],
                        'total':mbg,
                        'ans':ans,
                        'groupcode':dis['question'].block.code,
                        'code':dis['question'].qstcode,
                        'pos':dis['pos'],
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'term':term,
                        'subject':subject})


                elif category == 'others':#stale and others
                  

                    return render_to_response('CBT/othersprev.html',{'varuser':varuser, 'question':dis['question'],
                        'school':school,
                        'qq':dis['qq'],
                        'image':dis['image'],
                        'options':dis['options'],
                        'ans':ans,
                        'total':mbg,
                        'pos':dis['pos'],
                        'groupcode': groupcode,
                        'code':qstcode,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':klass,
                        'adm':student.admissionno,                            
                        'term':term,
                        'subject':subject})

            else:
                return HttpResponseRedirect('/welcome/')
        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')




def nabpush(request):
    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]

            code2 = request.POST['code']

            groupcode2 = request.POST['groupcode']

            student= Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)
            klass=student.admitted_class 
            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)
            subject=now_scheduled.subject

            
            cvcc = current_question(currse,term,subject,student,ex.exam_type)

            if cvcc['code']==code2 :


                pik = tblcbttranscomp.objects.get(student=student,session=currse,
                    term=term, exam_type=ex.exam_type,qno=cvcc['number'],subject=subject)

                # msg = pik   return render_to_response('CBT/selectloan.html',{'msg':msg})
                
                a=pik.stu_ans
                category=pik.category
                qstcode=pik.qstcode
                groupcode=pik.groupcode


                if 'gender' in request.POST:
                    a= request.POST['gender']


                if cvcc['category'] =='C':
                    myq=tblcomprehensionqst.objects.get(qstcode=cvcc['code'])
                    ans = tblanscomp.objects.get(qstn =myq).ans
                    
                elif cvcc['category']=='block':
                    myq=tblblockquestion.objects.get(qstcode=cvcc['code'])
                    ans = tblansblk.objects.get(qstn=myq).ans

              
                elif cvcc['category']== 'others':
                    myq=tblothers.objects.get(qstcode=cvcc['code'])
                    ans = tblansothers.objects.get(qstn=myq).ans


                if a == str(ans):
                    score =1
                else:
                    score=0


                myq = tblcbttranscomp.objects.filter(qstcode= cvcc['code'],student=student).update(score=score,stu_ans=a)
      


                n2=int(cvcc['number']) + 1

                mbg  = questioncount(currse,klass,term,subject,ex.exam_type)



                if n2 <= mbg:
                    


                    pik = tblcbttranscomp.objects.filter(student=student,session=currse,
                        term=term, exam_type=ex.exam_type,qno=n2,subject=subject)

                    
                    if pik.count() ==1:
                        pik = pik.get()
                    
                        ans=pik.stu_ans
                        category=pik.category
                        qstcode=pik.qstcode
                        groupcode=pik.groupcode


                      
                        cvcc['asd'].number = n2
                        cvcc['asd'].save()


                        cvcc['q_code'].qstno = n2
                        cvcc['q_code'].qstcode=qstcode
                        cvcc['q_code'].groupcode = groupcode
                        cvcc['q_code'].category = category
                        cvcc['q_code'].save()



                        tblcbtoldeng.objects.filter(question=cvcc['asd']).update(qstno=n2, qstcode=qstcode,groupcode=groupcode,category=category)

                        

                        dis = display_answered_qstn(qstcode,category,n2)


                        if category =='C':

                            myq=tblcomprehensionqst.objects.get(qstcode=qstcode)
                            opt = tbloptionseng.objects.get(qstn = myq)

                            return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':dis['question'],
                                'school':school,
                                'qq':dis['qq'],
                                'image':dis['image'],
                                'options':dis['options'],
                                'pos':dis['pos'],
                                'ans':ans,
                                'total':mbg,

                                'groupcode':'fu',
                                'code':dis['question'].qstcode,
                                'exam': ex.exam_type,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'term':term,
                                'subject':subject})#comprehension and others



                        elif category=='block':

                            myq = tblblockquestion.objects.get(qstcode=qstcode)


                            try :
                                opt = tbloptionblk.objects.get(qstn=myq)
                                pos = 'low'
                            except:
                                opt = tbloptionblki.objects.get(qstn = myq)
                                pos = 'hi'
                        
                            return render_to_response('CBT/blkprevious.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'qq':dis['qq'],
                                'options':dis['options'],
                                'total':mbg,
                                'ans':ans,
                                'groupcode':dis['question'].block.code,
                                'code':dis['question'].qstcode,
                                'pos':dis['pos'],
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'term':term,
                                'subject':subject})



                        elif category == 'others':#stale and others
                            myq = tblothers.objects.get(qstcode=qstcode)

                            try :
                                opt = tbloptionsothers.objects.get(qstn=myq)
                                pos = 'low'
                            except:
                                opt = tbloptionothersi.objects.get(qstn = myq)
                                pos = 'hi'


                            return render_to_response('CBT/othersprev.html',{'varuser':varuser, 'question':dis['question'],
                                'school':school,
                                'qq':dis['qq'],
                                'image':dis['image'],
                                'options':dis['options'],
                                'ans':ans,
                                'total':mbg,
                                'pos':dis['pos'],
                                'groupcode': groupcode,
                                'code':qstcode,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':klass,
                                'adm':student.admissionno,                            
                                'term':term,
                                'subject':subject})


                    else:
                        

                        ccp_code = Next_unanswered_compre_qst(currse,term,subject,student,ex.exam_type,'C',klass)


                        if ccp_code['question'] == 0 :

                            display_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)

                            if display_code['question'] == 0 :
                                return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                                    'groupcode':cvcc['groupcode'],
                                    'code':cvcc['code']})

                            
                            else:
                                myq =display_code['question']

                                ft = total_ans_qst(currse,term,subject,student,ex.exam_type)
                                next_no = ft - display_code['solved'] + 1
                                qq=  ft  + 1
                                to = ft + display_code['remain']


                                if display_code['groupcode'] !='AA': #for blk questions

                                    try :
                                        opt = tbloptionblk.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionblki.objects.get(qstn = myq)
                                        pos = 'hi'


                                    cvcc['asd'].number = qq
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = qq
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode = display_code['question'].block.code
                                    cvcc['q_code'].category = 'block' 
                                    cvcc['q_code'].save()



                                    return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'to': to,
                                        'qq':qq,
                                        'total':mbg,
                                        'pos':pos,
                                        'groupcode':display_code['question'].block.code,
                                        'code':display_code['question'].qstcode,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})
                                
                                else:    #for others questions             

                                    try :
                                        opt = tbloptionsothers.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionothersi.objects.get(qstn = myq)
                                        pos = 'hi'


                                    cvcc['asd'].number = qq
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = qq
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode = 'AA'
                                    cvcc['q_code'].category = 'others' 
                                    cvcc['q_code'].save()


                                    return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'qq':qq,
                                        'to': to,
                                        'total':mbg,
                                        'groupcode':'AA',
                                        'code':display_code['question'].qstcode,
                                        'pos':pos,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})


                        else:

                            # msg = 'im comprehension'         return render_to_response('CBT/selectloan.html',{'msg':msg})

                            myq = ccp_code['question'] 
                            opt = tbloptionseng.objects.get(qstn = myq)


                            ft = total_ans_qst(currse,term,subject,student,ex.exam_type)
                            next_no = ft - ccp_code['solved'] + 1
                            qq=  ft  + 1
                            to = ft + ccp_code['remain']



                            cvcc['asd'].number = qq
                            cvcc['asd'].save()


                            cvcc['q_code'].qstno = qq
                            cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                            cvcc['q_code'].groupcode = 'fu'
                            cvcc['q_code'].category = 'C' 
                            cvcc['q_code'].save()



                            return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'to': to,
                                'qq':qq,
                                'total':mbg,
                                'groupcode':'fu',
                                'code':ccp_code['question'].qstcode,
                                'form':student,
                                'session':currse,
                                'exam':ex.exam_type,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})


                else:
                    return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                        'groupcode':cvcc['groupcode'],
                        'code':cvcc['code']})

                    


            else:
                return HttpResponseRedirect('/welcome/')

        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')



def spin(request):

    if "userid" in request.session:        
        
        if request.method=='POST':

            varuser=request.session['userid']

            code2 = request.POST['code']
            groupcode2 = request.POST['groupcode']


            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)

            klass=student.admitted_class

            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)

            subject=now_scheduled.subject


            cvcc = current_question(currse,term,subject,student,ex.exam_type)

        
            if cvcc['code']==code2 :

                mbg  = questioncount(currse, klass,term,subject,ex.exam_type)

                if cvcc['category']== 'C':


                    ccp_code = spin_compre_qst(currse,term,subject,student,ex.exam_type,cvcc['category'],klass,code2)



                    myq = ccp_code['question'] 
                    opt = tbloptionseng.objects.get(qstn = myq)


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                    next_no = ft - ccp_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + ccp_code['remain']



                    cvcc['asd'].number = qq
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = qq
                    cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                    cvcc['q_code'].groupcode = 'fu'
                    cvcc['q_code'].category = 'C' 
                    cvcc['q_code'].save()


                    return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'to': to,
                        'qq':qq,
                        'total':mbg,
                        'groupcode':'fu',
                        'code':ccp_code['question'].qstcode,
                        'form':student,
                        'exam':ex.exam_type,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject}) 


                elif cvcc['category']=='block':     

                    ccp_code = spin_blk(currse,term,subject,student,ex.exam_type,'block',cvcc['groupcode'],klass,code2)
                    myq = ccp_code['question'] 
                    try :
                        opt = tbloptionblk.objects.get(qstn=myq)
                        pos = 'low'
                    except:
                        opt = tbloptionblki.objects.get(qstn = myq)
                        pos = 'hi'


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                    next_no = ft - ccp_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + ccp_code['remain']


                    cvcc['asd'].number = qq
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = qq
                    cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                    cvcc['q_code'].groupcode = ccp_code['question'].block.code
                    cvcc['q_code'].category = 'block' 
                    cvcc['q_code'].save()



                    return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'to': to,
                        'qq':qq,
                        'total':mbg,
                        'groupcode':ccp_code['question'].block.code,
                        'code':ccp_code['question'].qstcode,
                        'pos':pos,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})


                elif cvcc['category']== 'others':
                        

                    ccp_code = spin_others(currse,term,subject,student,ex.exam_type,klass,code2)

                                            
                    myq = ccp_code['question']                  

                    try :
                        opt = tbloptionsothers.objects.get(qstn=myq)
                        pos = 'low'
                    except:
                        opt = tbloptionothersi.objects.get(qstn = myq)
                        pos = 'hi'


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                    next_no = ft - ccp_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + ccp_code['remain']



                    cvcc['asd'].number = qq
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = qq
                    cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                    cvcc['q_code'].groupcode = 'AA'
                    cvcc['q_code'].category = 'others' 
                    cvcc['q_code'].save()


                    return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'qq':qq,
                        'to': to,
                        'total':mbg,
                        'groupcode':'AA',
                        'code':ccp_code['question'].qstcode,
                        'pos':pos,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})
        
            else: # if f = e

                return HttpResponseRedirect('/welcome/')

        else:


            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')


def wheel(request):
    if "userid" in request.session:
    
        
        if request.method=='POST':

            varuser=request.session['userid']


            code2 = request.POST['code']
            groupcode2 = request.POST['groupcode']


            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)

            klass=student.admitted_class

            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)

            subject=now_scheduled.subject


            cvcc = current_question(currse,term,subject,student,ex.exam_type)


            if cvcc['code']==code2 :

                mbg  = questioncount(currse, klass,term,subject,ex.exam_type)


                display_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)


                myq =display_code['question']

                if display_code['groupcode'] !='AA': #for blk questions

                    try :
                        opt = tbloptionblk.objects.get(qstn=myq)
                        pos = 'low'
                    except:
                        opt = tbloptionblki.objects.get(qstn = myq)
                        pos = 'hi'


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                    next_no = ft - display_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + display_code['remain']             




                    cvcc['asd'].number = next_no
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = next_no
                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                    cvcc['q_code'].groupcode =display_code['question'].block.code
                    cvcc['q_code'].category = 'block' 
                    cvcc['q_code'].save()



                    return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'to': to,
                        'qq':qq,
                        'total':mbg,
                        'pos':pos,
                        'groupcode':display_code['question'].block.code,
                        'code':display_code['question'].qstcode,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})
                
                else:    #for others questions             

                    try :
                        opt = tbloptionsothers.objects.get(qstn=myq)
                        pos = 'low'
                    except:
                        opt = tbloptionothersi.objects.get(qstn = myq)
                        pos = 'hi'


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                    next_no = ft - display_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + display_code['remain']




                    cvcc['asd'].number = qq
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = qq
                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                    cvcc['q_code'].groupcode = 'AA'
                    cvcc['q_code'].category = 'others' 
                    cvcc['q_code'].save()


                    return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'qq':qq,
                        'to': to,
                        'total':mbg,
                        'groupcode':'AA',
                        'code':display_code['question'].qstcode,
                        'pos':pos,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})



            else:
                return HttpResponseRedirect('/welcome/')



        else:


            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')




def engnext(request):

    if "userid" in request.session:        
        
        if request.method=='POST':

            varuser=request.session['userid']

            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)

            klass=student.admitted_class

            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)

            subject=now_scheduled.subject


            cvcc = current_question(currse,term,subject,student,ex.exam_type)

          
            
            if 'gender' in request.POST: #if option is selected
                a= request.POST['gender']
                code2 = request.POST['code']
                groupcode2 = request.POST['groupcode']
                


                if cvcc['code']==code2 :

                    mbg  = questioncount(currse, klass,term,subject,ex.exam_type)

                    if cvcc['category']== 'C':

                        myq=tblcomprehensionqst.objects.get(qstcode=cvcc['code'])

                        ans = tblanscomp.objects.get(qstn =myq).ans


                        if a == str(ans):
                            score =1
                        else:
                            score=0


                        tblcbttranscomp( session =currse, exam_type =ex.exam_type,
                            student = student, subject = subject,
                            term = term, stu_ans = a, score = score,
                            status =1, qno = cvcc['number'],qstcode = cvcc['code'], category=cvcc['category'],
                            groupcode = 'fu' ).save()


                        ccp_code = Next_unanswered_compre_qst(currse,term,subject,student,ex.exam_type,cvcc['category'],klass)


                        if ccp_code['question'] == 0 :

                            display_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)

                            if display_code['question'] == 0 :
                                return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                                    'groupcode':cvcc['groupcode'],
                                    'code':cvcc['code']})

                            
                            else:

                                myq =display_code['question']

                                if display_code['groupcode'] !='AA': #for blk questions

                                    try :
                                        opt = tbloptionblk.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionblki.objects.get(qstn = myq)
                                        pos = 'hi'


                                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                                    next_no = ft - display_code['solved'] + 1
                                    qq=  ft  + 1

                                    to = ft + display_code['remain']


                                    cvcc['asd'].number = next_no
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = next_no
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode = display_code['question'].block.code
                                    cvcc['q_code'].category = 'block' 
                                    cvcc['q_code'].save()



                                    return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'to': to,
                                        'qq':qq,
                                        'total':mbg,
                                        'pos':pos,
                                        'groupcode':display_code['question'].block.code,
                                        'code':display_code['question'].qstcode,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})
                                
                                else:    #for others questions             

                                    try :
                                        opt = tbloptionsothers.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionothersi.objects.get(qstn = myq)
                                        pos = 'hi'


                                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                                    next_no = ft - display_code['solved'] + 1
                                    qq=  ft  + 1

                                    to = ft + display_code['remain']


                                    cvcc['asd'].number = qq
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = qq
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode = 'AA'
                                    cvcc['q_code'].category = 'others' 
                                    cvcc['q_code'].save()


                                    return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'qq':qq,
                                        'to': to,
                                        'total':mbg,
                                        'groupcode':'AA',
                                        'code':display_code['question'].qstcode,
                                        'pos':pos,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})


                        else:


                            myq = ccp_code['question'] 
                            opt = tbloptionseng.objects.get(qstn = myq)


                            ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                            next_no = ft - ccp_code['solved'] + 1
                            qq=  ft  + 1

                            to = ft + ccp_code['remain']



                            cvcc['asd'].number = qq
                            cvcc['asd'].save()


                            cvcc['q_code'].qstno = qq
                            cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                            cvcc['q_code'].groupcode = 'fu'
                            cvcc['q_code'].category = 'C' 
                            cvcc['q_code'].save()





                            return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'to': to,
                                'qq':qq,
                                'total':mbg,
                                'groupcode':'fu',
                                'code':ccp_code['question'].qstcode,
                                'form':student,
                                'exam':ex.exam_type,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})


                    elif cvcc['category']=='block':
                        solvedd = request.POST['solved']


                        myq=tblblockquestion.objects.get(qstcode=cvcc['code'])

                        ans = tblansblk.objects.get(qstn=myq).ans

                        # msg = a, ans return render_to_response('CBT/selectloan.html',{'msg':msg})


                        if a == str(ans):
                            score =1
                        else:
                            score=0

                        # qno = int(cvcc['number']) + int(solvedd)


                        tblcbttranscomp( session =currse, exam_type =ex.exam_type,
                            student = student, subject = subject,
                            term = term, stu_ans = a, score = score,
                            status =1, qno = solvedd , qstcode = cvcc['code'], 
                            category=cvcc['category'],  groupcode = cvcc['groupcode'] ).save()


                        

                        ccp_code=Next_unanswered_blk2_question(currse,term,subject,student,ex.exam_type,'block',cvcc['groupcode'],klass)

                        if ccp_code['question'] == 0 :

                            display_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)

                            if display_code['question'] == 0 :
                                return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                                    'groupcode':cvcc['groupcode'],
                                    'code':cvcc['code']})
                            
                            else:

                                myq =display_code['question']

                                if display_code['groupcode'] !='AA': #for blk questions

                                    try :
                                        opt = tbloptionblk.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionblki.objects.get(qstn = myq)
                                        pos = 'hi'


                                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                                    next_no = ft - display_code['solved'] + 1
                                    qq=  ft  + 1

                                    to = ft + display_code['remain']             




                                    cvcc['asd'].number = next_no
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = next_no
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode =display_code['question'].block.code
                                    cvcc['q_code'].category = 'block' 
                                    cvcc['q_code'].save()



                                    return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'to': to,
                                        'qq':qq,
                                        'total':mbg,
                                        'pos':pos,
                                        'groupcode':display_code['question'].block.code,
                                        'code':display_code['question'].qstcode,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})
                                
                                else:    #for others questions             

                                    try :
                                        opt = tbloptionsothers.objects.get(qstn=myq)
                                        pos = 'low'
                                    except:
                                        opt = tbloptionothersi.objects.get(qstn = myq)
                                        pos = 'hi'


                                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                                    next_no = ft - display_code['solved'] + 1
                                    qq=  ft  + 1

                                    to = ft + display_code['remain']




                                    cvcc['asd'].number = qq
                                    cvcc['asd'].save()


                                    cvcc['q_code'].qstno = qq
                                    cvcc['q_code'].qstcode=display_code['question'].qstcode
                                    cvcc['q_code'].groupcode = 'AA'
                                    cvcc['q_code'].category = 'others' 
                                    cvcc['q_code'].save()


                                    return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                        'school':school,
                                        'count':next_no,
                                        'qq':qq,
                                        'to': to,
                                        'total':mbg,
                                        'groupcode':'AA',
                                        'code':display_code['question'].qstcode,
                                        'pos':pos,
                                        'form':student,
                                        'session':currse,
                                        'name':student.admissionno,
                                        'klass':student.admitted_class,
                                        'adm':student.admissionno,
                                        'options':opt,
                                        'term':term,
                                        'subject':subject})


                        else:
                            
                            myq = ccp_code['question'] 
                            try :
                                opt = tbloptionblk.objects.get(qstn=myq)
                                pos = 'low'
                            except:
                                opt = tbloptionblki.objects.get(qstn = myq)
                                pos = 'hi'


                            ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                            next_no = ft - ccp_code['solved'] + 1
                            qq=  ft  + 1

                            to = ft + ccp_code['remain']




                            cvcc['asd'].number = qq
                            cvcc['asd'].save()


                            cvcc['q_code'].qstno = qq
                            cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                            cvcc['q_code'].groupcode = ccp_code['question'].block.code
                            cvcc['q_code'].category = 'block' 
                            cvcc['q_code'].save()



                            return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'to': to,
                                'qq':qq,
                                'total':mbg,
                                'groupcode':ccp_code['question'].block.code,
                                'code':ccp_code['question'].qstcode,
                                'pos':pos,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})

                    elif cvcc['category']== 'others':
                        myq=tblothers.objects.get(qstcode=cvcc['code'])

                        ans = tblansothers.objects.get(qstn=myq).ans

                        # msg = a, ans return render_to_response('CBT/selectloan.html',{'msg':msg})


                        if a == str(ans):
                            score =1
                        else:
                            score=0


                        tblcbttranscomp( session =currse, exam_type =ex.exam_type,
                            student = student, subject = subject,
                            term = term, stu_ans = a, score = score,
                            status =1, qno = cvcc['number'],qstcode = cvcc['code'], 
                            category='others',  groupcode = 'AA').save()


                        ccp_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)
                
                        myq =ccp_code['question']
                       
                        if myq == 0 :
                            return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                                'groupcode':cvcc['groupcode'],
                                'code':cvcc['code']})
                        
                        else:

                            if ccp_code['groupcode'] !='AA': #if i am block                                  


                                try :
                                    opt = tbloptionblk.objects.get(qstn=myq)
                                    pos = 'low'
                                except:
                                    opt = tbloptionblki.objects.get(qstn = myq)
                                    pos = 'hi'


                                ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                                next_no = ft - ccp_code['solved'] + 1
                                qq=  ft  + 1

                                to = ft + ccp_code['remain']             



                                cvcc['asd'].number = next_no
                                cvcc['asd'].save()


                                cvcc['q_code'].qstno = next_no
                                cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                                cvcc['q_code'].groupcode = ccp_code['question'].block.code
                                cvcc['q_code'].category = 'block' 
                                cvcc['q_code'].save()



                                return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                    'school':school,
                                    'count':next_no,
                                    'to': to,
                                    'qq':qq,
                                    'total':mbg,
                                    'pos':pos,
                                    'groupcode':ccp_code['question'].block.code,
                                    'code':ccp_code['question'].qstcode,
                                    'form':student,
                                    'session':currse,
                                    'name':student.admissionno,
                                    'klass':student.admitted_class,
                                    'adm':student.admissionno,
                                    'options':opt,
                                    'term':term,
                                    'subject':subject})
                            
                            else:        #if i am others      

                                try :
                                    opt = tbloptionsothers.objects.get(qstn=myq)
                                    pos = 'low'
                                except:
                                    opt = tbloptionothersi.objects.get(qstn = myq)
                                    pos = 'hi'


                                ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                                next_no = ft - ccp_code['solved'] + 1
                                qq=  ft  + 1

                                to = ft + ccp_code['remain']




                                cvcc['asd'].number = qq
                                cvcc['asd'].save()


                                cvcc['q_code'].qstno = qq
                                cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                                cvcc['q_code'].groupcode = 'AA'
                                cvcc['q_code'].category = 'others' 
                                cvcc['q_code'].save()



                                return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                    'school':school,
                                    'count':next_no,
                                    'qq':qq,
                                    'to': to,
                                    'total':mbg,
                                    'groupcode':'AA',
                                    'code':ccp_code['question'].qstcode,
                                    'pos':pos,
                                    'form':student,
                                    'session':currse,
                                    'name':student.admissionno,
                                    'klass':student.admitted_class,
                                    'adm':student.admissionno,
                                    'options':opt,
                                    'term':term,
                                    'subject':subject})


                else:
                    return HttpResponseRedirect('/welcome/')

            
            else: #if i didnt chose an option

                return HttpResponseRedirect('/welcome/')

        else:


            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')


def renew(request):
    if "userid" in request.session:        
        
        if request.method=='POST':

            varuser=request.session['userid']

            code2 = request.POST['code']
            groupcode2 = request.POST['groupcode']


            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)

            klass=student.admitted_class

            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)

            subject=now_scheduled.subject

            cvcc = current_question(currse,term,subject,student,ex.exam_type)

            if cvcc['code']==code2 :


                mbg  = questioncount(currse, student.admitted_class,term,subject,ex.exam_type)

                ccp_code = Next_unanswered_compre_qst(currse,term,subject,student,ex.exam_type,'C',klass)


                if ccp_code['question'] == 0 :

                    display_code = transition_blk_others(currse,term,subject,student,ex.exam_type,klass)

                    if display_code['question'] == 0 :
                        
                        totala = tblcbttranscomp.objects.get(session=currse,term=term,
                            subject=subject,exam_type=ex.exam_type,student=student,qno =mbg)


                        cvcc['asd'].number = mbg
                        cvcc['asd'].save()


                        cvcc['q_code'].qstno = mbg
                        cvcc['q_code'].qstcode= totala.qstcode
                        cvcc['q_code'].groupcode = totala.groupcode
                        cvcc['q_code'].category = totala.category 
                        cvcc['q_code'].save()

                        return render_to_response('CBT/englishdone.html',{'varuser':varuser,
                            'groupcode':totala.groupcode,
                            'code':totala.qstcode})

                    else:

                        myq =display_code['question']

                        if display_code['groupcode'] !='AA': #for blk questions

                            try :
                                opt = tbloptionblk.objects.get(qstn=myq)
                                pos = 'low'
                            except:
                                opt = tbloptionblki.objects.get(qstn = myq)
                                pos = 'hi'


                            ft = total_ans_qst(currse,term,subject,student,ex.exam_type)

                            next_no = ft - display_code['solved'] + 1
                            qq=  ft  + 1

                            to = ft + display_code['remain']


                            cvcc['asd'].number = qq
                            cvcc['asd'].save()


                            cvcc['q_code'].qstno = qq
                            cvcc['q_code'].qstcode=display_code['question'].qstcode
                            cvcc['q_code'].groupcode = display_code['question'].block.code
                            cvcc['q_code'].category = 'block' 
                            cvcc['q_code'].save()



                            return render_to_response('CBT/currentblk.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'to': to,
                                'qq':qq,
                                'total':mbg,
                                'pos':pos,
                                'groupcode':display_code['question'].block.code,
                                'code':display_code['question'].qstcode,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})
                        
                        else:    #for others questions             

                            try :
                                opt = tbloptionsothers.objects.get(qstn=myq)
                                pos = 'low'
                            except:
                                opt = tbloptionothersi.objects.get(qstn = myq)
                                pos = 'hi'


                            ft = total_ans_qst(currse,term,subject,student,ex.exam_type)           


                            next_no = ft - display_code['solved'] + 1
                            qq=  ft  + 1

                            to = ft + display_code['remain']


                            cvcc['asd'].number = qq
                            cvcc['asd'].save()


                            cvcc['q_code'].qstno = qq
                            cvcc['q_code'].qstcode=display_code['question'].qstcode
                            cvcc['q_code'].groupcode = 'AA'
                            cvcc['q_code'].category = 'others' 
                            cvcc['q_code'].save()


                            return render_to_response('CBT/currentothers.html',{'varuser':varuser, 'question':myq,
                                'school':school,
                                'count':next_no,
                                'qq':qq,
                                'to': to,
                                'total':mbg,
                                'groupcode':'AA',
                                'code':display_code['question'].qstcode,
                                'pos':pos,
                                'form':student,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})


                else:


                    myq = ccp_code['question'] 
                    opt = tbloptionseng.objects.get(qstn = myq)


                    ft = total_ans_qst(currse,term,subject,student,ex.exam_type)


                    next_no = ft - ccp_code['solved'] + 1
                    qq=  ft  + 1

                    to = ft + ccp_code['remain']



                    cvcc['asd'].number = qq
                    cvcc['asd'].save()


                    cvcc['q_code'].qstno = qq
                    cvcc['q_code'].qstcode=ccp_code['question'].qstcode
                    cvcc['q_code'].groupcode = 'fu'
                    cvcc['q_code'].category = 'C' 
                    cvcc['q_code'].save()

                    return render_to_response('CBT/currentcomp.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':next_no,
                        'to': to,
                        'qq':qq,
                        'total':mbg,
                        'groupcode':'fu',
                        'code':ccp_code['question'].qstcode,
                        'form':student,
                        'session':currse,
                        'exam':ex.exam_type,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})

            else:
                return HttpResponseRedirect('/welcome/')
            

        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')


def prenext(request):

    if "userid" in request.session:        
        
        # if request.method=='POST':


        varuser=request.session['userid']
        student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)
        klass=student.admitted_class
        

        ex=tblcbtexams.objects.get(status='ACTIVE')

        now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)

        subject=now_scheduled.subject
        

        disp_no = tblcbtcurrentquestioneng.objects.get(session=currse,term=term,
            subject=subject,student=student, exam_type=ex.exam_type)


        disp_no_number = disp_no.number
        
        disp_qst = tblcbtoldeng.objects.get(question=disp_no)
        disp_qst_category  = disp_qst.category

        ccc =[disp_qst.qstcode]


        if 'gender' in request.POST: #if option is selected
            a= request.POST['gender']

            opt = tbloptionseng.objects.get(qstn = myq)
            ans = tblanscomp.objects.get(qstn =myq).ans

            number=disp_no_number

            image= myq.comprehension.qstimage

            pos='pos'
            
            img='img'

            return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':myq,
                'school':school,
                'count':number,
                'image':img,
                'pos':image,
                'ans':ans,

                'groupcode':'fu',
                'code':dis['question'].qstcode,
                'exam': ex.exam_type,

                'questioncount':qcount,
                'form':student,
                'session':currse,
                'name':student.admissionno,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'subject':subject})
                
        
        else: #if i didnt chose an option


            next_no_number = disp_no.number+1

            try:



                mansd = tblcbttranscomp.objects.get(session=currse,
                            exam_type=ex.exam_type,
                            student=student,
                            subject=subject,
                            term=term,
                            qno =next_no_number,
                            category=disp_qst_category)

                if mansd.category =='C' :

                    myq = tblcomprehensionqst.objects.get(qstcode=mansd.qstcode)




                    opt = tbloptionseng.objects.get(qstn = myq)
                    ans = tblanscomp.objects.get(qstn =myq).ans

                    number=disp_no_number

                    image= myq.comprehension.qstimage

                    pos='pos'
                    
                    img='img'

                    return render_to_response('CBT/curen2gl.html',{'varuser':varuser, 'question':myq,
                        'school':school,
                        'count':number,
                        'image':img,
                        'pos':image,
                        'ans':ans,

                        'groupcode':'fu',
                        'code':dis['question'].qstcode,
                        'exam': ex.exam_type,
                        'questioncount':qcount,
                        'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'subject':subject})

                elif mansd.category =='block' :
                    dfvdvf=7

                elif mansd.category =='others' :
                    dgf=4




                #display it

            except: 


                d=0 







            return HttpResponseRedirect('/welcome/')


        # else:


        #     return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')






def guides(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,term,klass,subject,exam_type= acccode.split(':')
                qst=[]
                myqst=tblquestion.objects.filter(session=session,
                    term=term,
                    klass=klass,
                    subject=subject,
                    exam_type=exam_type).order_by('klass')

                for q in myqst:
                    try:
                        myanswer = tblans.objects.get(qstn=q)
                        myanswer=myanswer.option
                    except:
                        myanswer='No Ans'
                    pair={'qst':q,'answer':myanswer}
                    qst.append(pair)

                # a,b = divmod(qst,15)


                return render_to_response('CBT/myguide.html',{'myqst':qst,
                'term':term,'subject':subject,'exam':exam_type,'klass':klass,'session':session})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getcbtsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = tblcbtuser.objects.filter(session=session,klass = klass,email = varuser )
                for j in data:
                    j = j.subject
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                   # print 'The Subject :',p
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



def getterm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                term=tblterm.objects.get(status='ACTIVE')
                term=term.term
                # data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state,term=term)
                # for j in data:
                #     j = j.term
                #     #print j
                #     s = {j:j}
                #     sdic.update(s)
                # klist = sdic.values()
                # klist.sort()
                # for p in klist:
                kk.append(term)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def ajaxclass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # state = acccode
                kk = []
                sdic = {}
                data = tblcbtuser.objects.filter(email = varuser,session = acccode).order_by('klass')
                for j in data:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
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


def exxxam(request):

## A SUBJECT MUST BE SCHEDULLED BEFORE IT CAN BE AVAILABLE FOR WRITITING
    if "userid" in request.session:

        varuser=request.session['userid'] #varuser is a list
        exam=tblcbtexams.objects.get(status='ACTIVE') #exam is a set


#current student
        pop =Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)

    

## STUDEnT's subject list
        akrec = StudentAcademicRecord.objects.get(student=pop,term=term)
        subs = SubjectScore.objects.filter(academic_rec=akrec,term=term)    
        stusub = [str(d.subject) for d in subs]

##All scheduled subjects for the day
        mydate=date.today()        
        
        activesub = tblcbtsubject.objects.filter(exam_type=exam.exam_type,
            st_date=mydate, session=currse,
            klass=pop.admitted_class,
            term=term).order_by('st_time')

        schesub =[str(k.subject) for k in activesub]



##already written subjects by student
        donsub=donesubjects.objects.filter(student=pop,
            exam_type=exam.exam_type,
            term=term,session=currse)

        ritensub =[str(d.subject) for d in donsub] 

#***********UNWRITTEN********************** 
        qu= [item for item in stusub if item not in ritensub]



        if qu == []:
            msg= 'YOU HAVE WRITTEN ALL YOUR PAPERS!! YOU MAY GO CHECK YOUR SCRPITS'
            return render_to_response('CBT/nosub.html',{'varerr':msg})


#*********************UNWRITTEN AND SCHEDULED************** 
        qp= [item for item in qu if item in schesub]

        
        if qp == []:
            msg= 'HELLO NO PAPER HAS BEEN SCHEDULED FOR YOU. CONTACT THE ADMIN'

            return render_to_response('CBT/nosub.html',{'varerr':msg})


#***************NOW SCHEDULLED*****************my banger

        current_time= datetime.time(datetime.now()) #extract current time from datetime


        alltime = []
        ended = 0
        notstarted=0
        for kl in qp:
            subject = kl
            vkva = tblcbtsubject.objects.get(exam_type=exam.exam_type,
                st_date=mydate, 
                session=currse,
                klass=pop.admitted_class,
                term=term,subject=kl) #where scheduled subjects are kept


            startimme=  vkva.st_time
            hr =startimme.hour
            mn = startimme.minute

            duration=int(vkva.duration)
            whole, remainder = divmod(duration,60)

            if remainder==0:
                if whole==1:
                    ddd=str(whole)+' hr'
                elif whole > 1:
                    ddd=str(whole)+' hrs'

            else:
                if whole==1:
                    ddd=str(whole)+' hr'+ " "+ str(remainder) + ' mins'
                
                elif whole > 1:
                    ddd=str(whole)+' hrs'+ " "+ str(remainder) + ' mins'

                elif whole < 1:
                    ddd= str(remainder) + ' mins'


            w1,r1 = divmod(mn+remainder,60)

            enndtime = time(hr+whole+w1,r1,0) #time constructor

            if startimme <= current_time:
                if     current_time < enndtime:

                    if kl =='ENGLISH' or kl == 'ENGLISH LANGUAGE':


                        mbg  = questioncount(currse, pop.admitted_class,term,subject,exam.exam_type)
                       

                    else:


                        qsts = tblquestion.objects.filter(subject=kl, 
                            session=currse,
                            klass=pop.admitted_class,
                            term=term,
                            exam_type=exam.exam_type,
                            section ='A')

                        mbg = qsts.count()


                    if mbg==0 : 
                        msg= 'NO QUESTIONS FOUND FOR  ' +  kl 
                        return render_to_response('CBT/nosub.html',{'varerr':msg, 'varuser':varuser,})



#KEEPING A SAFE OF NOW SCHEDULLED subject
                    try:
                        now_schedulled = scheduled.objects.get(student=pop,
                            session=currse,term=term,
                            assessment=exam.exam_type,
                            subject=kl)

                    except:
                        scheduled(student=pop,session=currse,
                            term=term,
                            assessment=exam.exam_type,
                            subject=kl).save()

#CASE 1. CHECK ACCREDITATION TABLE FOR CODE(OCCURRENCE)
#IF ITS FOUND, ASK USER OF IT
#CASE2:
#ELSE, GENERATE A RANDOM NO, SAVE IT AND REDIRECT TO ANOTHER PAGE 
#WHERE DJANGO WILL DEMAND FOR IT

#GENERATE ACCREDITATION COD FOR THIS EXAM 
#AND KEEP IT SAFE

                    if kl == 'ENGLISH' or kl == 'ENGLISH LANGUAGE':
                        return render_to_response('CBT/cbteng.html',{'term':term,
                            'varuser':varuser,
                            'sch':school,
                            'qu':enndtime,
                            'duration':ddd,
                            'qp':mbg,
                            'qpick':vkva,
                            'pop':pop,'exam':exam.exam_type})
                    else:


                        return render_to_response('CBT/cbt.html',{'term':term,
                            'varuser':varuser,
                            'sch':school,
                            'qu':enndtime,
                            'duration':ddd,
                            'qp':mbg,
                            'qpick':vkva,
                            'pop':pop,'exam':exam.exam_type})

                else:
                    ended+=1
            else:
                notstarted+=1
        if ended> 0 or notstarted>0:
            msg= 'ALL THE PAPERS SCHEDULED FOR TODAY HAS BEEN WRITTEN' 
            return render_to_response('CBT/nosub.html',{'varerr':msg, 'varuser':varuser,})



                
    else:
        return HttpResponseRedirect('/login/')





def beefore(request):
    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]
            student= Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)
            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)
            subject=now_scheduled.subject
            
            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)

            number=int(qc.number)
            
            if number==1:
                
                try:
                    pik = cbttrans.objects.get(student=student,session=currse,term=term,               
                    exam_type=ex.exam_type,no=number,subject=subject)
                    ans=pik.stu_ans
                    g='ttt'
                except:
                    pik=cbtold.objects.get(student=student,
                        session=currse,
                        term=term,
                        klass=student.admitted_class,
                        subject=subject,
                        exam_type=ex.exam_type)
                    ans=''
                    g='fff'
                
                tk = tblquestion.objects.get(
                    session=currse,
                    term=term, 
                    klass=student.admitted_class,
                    exam_type=ex.exam_type, 
                    subject=subject,
                    id=pik.qstcode)

                tk1 =tk.qstn
                tk2=tk.id
                img=tk.image

                k = tbloptions.objects.filter(qstn=tk).count()
                if k == 0:
                    opt = tbloptioni.objects.filter(qstn=tk)
                    image='hi'
                else:
                    opt = tbloptions.objects.filter(qstn=tk)
                    image='low'

                if g == 'fff':
                    return render_to_response('CBT/pupiltest.html',{'question':tk1,
                        'school':school, 'count':number, 'pos':image,
                        'ans':ans,'image':img, 'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'uid':tk.id,
                        'subject':subject})
                elif g =='ttt':
                    return render_to_response('CBT/previous.html',{'question':tk1,
                        'school':school,'count':number,'pos':image,
                        'ans':ans,'image':img,'form':student,
                        'session':currse,
                        'name':student.admissionno,
                        'klass':student.admitted_class,
                        'adm':student.admissionno,
                        'options':opt,
                        'term':term,
                        'uid':tk.id,
                        'subject':subject})

            else:
                n2=number-1
                pik = cbttrans.objects.get(student=student,session=currse,term=term,               
                exam_type=ex.exam_type,no=n2,subject=subject)
                ans=pik.stu_ans
              
                qc.number=n2
                qc.save()
                number=n2

            tk = tblquestion.objects.get(
                session=currse,
                term=term, 
                klass=student.admitted_class,
                exam_type=ex.exam_type, 
                subject=subject,
                id=pik.qstcode)


            tk1 =tk.qstn
            tk2=tk.id
            img=tk.image

            k = tbloptions.objects.filter(qstn=tk).count()
            if k == 0:
                opt = tbloptioni.objects.filter(qstn=tk)
                image='hi'
            else:
                opt = tbloptions.objects.filter(qstn=tk)
                image='low'
                      
            
            return render_to_response('CBT/previous.html',{'question':tk1,
                'school':school,
                'count':number,
                'pos':image,
                'ans':ans,
                'image':img,
                'form':student,
                'session':currse,
                'name':student.admissionno,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'uid':tk.id,
                'subject':subject})

        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')



def donebee(request):
    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]
            student= Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)
            ex=tblcbtexams.objects.get(status='ACTIVE')

            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)
            subject=now_scheduled.subject
            
            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)

            number=int(qc.number)
            

            pik = cbttrans.objects.get(student=student,session=currse,term=term,               
            exam_type=ex.exam_type,no=number,subject=subject)
            ans=pik.stu_ans
                  
            tk = tblquestion.objects.get(session=currse,term=term, klass=student.admitted_class,
                exam_type=ex.exam_type, subject=subject,id=pik.qstcode)

            tk1 =tk.qstn
            tk2=tk.id
            img=tk.image

            k = tbloptions.objects.filter(qstn=tk).count()
            if k == 0:
                opt = tbloptioni.objects.filter(qstn=tk)
                image='hi'
            else:
                opt = tbloptions.objects.filter(qstn=tk)
                image='low'

            
            return render_to_response('CBT/previous.html',{'question':tk1,
                'school':school,
                'count':number,
                'pos':image,
                'ans':ans,
                'image':img,
                'form':student,
                'session':currse,
                'name':student.admissionno,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'uid':tk.id,
                'subject':subject})

        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')





def qtheory(request):
    if "userid" in request.session:        
        
    # if request.method=='POST':
        varuser=request.session['userid']
        student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)
        
        ex=tblcbtexams.objects.get(status='ACTIVE')
        
        try:
            now_scheduled= scheduled.objects.get(student=student,
                term=term,assessment=ex.exam_type,
                session=currse)
            subject=now_scheduled.subject

        except:
            msg= 'SEEMS YOU ALREADY SUBMITTED YOUR WORK!!!'
            return render_to_response('CBT/nosub.html',{'varerr':msg})

        qstns=tbltheory.objects.filter(term=term,exam_type=ex.exam_type,
            session=currse,subject=subject,
            klass=student.admitted_class)


        return render_to_response('CBT/qth.html',{'question':qstns,
                    'school':school,'form':student,'session':currse,
                    'name':student.admissionno, 'klass':student.admitted_class,
                    'adm':student.admissionno, 'term':term,'subject':subject})


    else:
        return HttpResponseRedirect('/login/')




def submitnext(request):
    if "userid" in request.session:        
        
        if request.method=='POST':
            varuser=request.session['userid']
            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)
            
            ex=tblcbtexams.objects.get(status='ACTIVE')
            
            try:
                now_scheduled= scheduled.objects.get(student=student,
                    term=term,assessment=ex.exam_type,
                    session=currse)
                subject=now_scheduled.subject

            except:
                msg= 'SOMETHING WENT WRONG!!! CONTACT THE HEAD OF I.T'
                return render_to_response('CBT/nosub.html',{'varerr':msg})

            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)

            # number=int(qc.number)

            qc.delete()
            now_scheduled.delete()
            donsub=donesubjects(student=student,
                exam_type=ex.exam_type, 
                subject=subject, term=term,session=currse).save()


            return render_to_response('CBT/submit.html')
        else:
            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')



def skip(request):
    if "userid" in request.session:
        if request.method=='POST':
            varuser=request.session["userid"]

            student= Student.objects.get(admissionno=varuser,admitted_session=currse,gone=False)
            ex=tblcbtexams.objects.get(status='ACTIVE')
            now_scheduled= scheduled.objects.get(student=student,term=term,assessment=ex.exam_type,session=currse)
            subject=now_scheduled.subject
            

            qstntys=tblquestion.objects.filter(term=term,exam_type=ex.exam_type,session=currse,subject=subject,klass=student.admitted_class)
            qcount=qstntys.count()


            qc=cbtcurrentquestion.objects.get(student=student, term =term,subject=subject,session=currse,exam_type=ex.exam_type)

            number=int(qc.number)
            current_q=cbtold.objects.get(session=currse,term=term, exam_type=ex.exam_type,klass=student.admitted_class,subject=subject,student=student)

            try:
                tk = cbttrans.objects.get(student=student,session=currse,term=term,exam_type=ex.exam_type,no=number,subject=subject)
                ans=tk.stu_ans
                seen = 'tim'
            except:
                seen = 'tom'            

            if seen == 'tom': # SKIPPED FROM FRESH QUESTON

##generate another random question from the pool

##COLLECTING ANSWERED QUESTIONS BY ID
                transid=[]
                trans=cbttrans.objects.filter(session=currse,exam_type=ex.exam_type,student=student,subject=subject,term=term)
                transid=[int(r.qstcode) for r in trans]

##COLLECTING SET QUESTIONS BY ID

                qstns=tblquestion.objects.filter(term=term,exam_type=ex.exam_type,session=currse,subject=subject,klass=student.admitted_class)
                myq=[]
                myq=[int(r.id) for r in qstns]

#DETECTING CURRENT QUESTION
                cntq=[]
                cntq=[int(current_q.qstcode)]

##SORTING OUT UNIQUE QUESTIONS
                qu=[]
                qu= [item for item in myq  if item not in transid]

    #Take away cuurent question
                qu= [item for item in qu  if item not in cntq]


                if qu != []:
##PICKING A RANDOM UNIQUE QUESTION BY ID
                    uid = 0
                    uid = random.choice(qu)
                    # tk=0
                    
                    tk = tblquestion.objects.get(id=uid)
#delete old question
                    current_q.delete()

                    cbtold(session=currse,question=tk,term=term,exam_type=ex.exam_type,klass=student.admitted_class,subject=subject,student=student, qstcode=tk.id).save()

                else:
                    tk=tblquestion.objects.get(id=current_q.qstcode)
            
               
                tk1 =tk.qstn
                k = tbloptions.objects.filter(qstn=tk).count()
                if k == 0:
                    opt = tbloptioni.objects.filter(qstn=tk)
                    image='hi'
                else:
                    opt = tbloptions.objects.filter(qstn=tk)
                    image='low'

                img=tk.image
                ans=''
                
            elif seen == 'tim':
                
                tk=tblquestion.objects.get(id=tk.qstcode)#student.admitted_class
                tk1 =tk.qstn

                k = tbloptions.objects.filter(qstn=tk).count()
                if k == 0:
                    opt = tbloptioni.objects.filter(qstn=tk)
                    image='hi'
                else:
                    opt = tbloptions.objects.filter(qstn=tk)
                    image='low'


                img=tk.image
                
            return render_to_response('CBT/pupiltest.html',{'question':tk1,
                'school':school,
                'count':number,
                'pos':image,
                'ans':ans,
                'image':img,
                'form':student,
                'session':currse,
                'name':student.admissionno,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'questioncount':qcount,
                'uid':tk.id,
                'subject':subject})

        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/login/')





def next(request):
    if "userid" in request.session:        
        
        if request.method=='POST':
            varuser=request.session['userid']
            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)
            
            ex=tblcbtexams.objects.get(status='ACTIVE')
            
            try:
                now_scheduled= scheduled.objects.get(student=student,
                    term=term,assessment=ex.exam_type,
                    session=currse)
                subject=now_scheduled.subject

            except:
                msg= 'SOMETHING WENT WRONG!!! CONTACT THE HEAD OF I.T'
                return render_to_response('CBT/nosub.html',{'varerr':msg})

            qstns=tblquestion.objects.filter(
                term=term,
                exam_type=ex.exam_type,
                session=currse,
                subject=subject,
                klass=student.admitted_class)

            qcount=qstns.count()


            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)
            number=int(qc.number)


            mycount = cbttrans.objects.filter(student=student,session=currse,
                    term=term, exam_type=ex.exam_type,
                    subject=subject)

#if i choose an answer
            if 'gender' in request.POST: #if option is selected
                a= request.POST['gender']
                    
                try:
                    dt = cbttrans.objects.get(student=student,session=currse,
                        term=term,exam_type=ex.exam_type,
                        no=number,subject=subject)
                    ty='update'
                except:                 
                    dt=cbtold.objects.get(student=student,session=currse,
                        term=term,exam_type=ex.exam_type,
                        klass=student.admitted_class,subject=subject)
                    ty='save'
                
                # selq= tblquestion.objects.get(session=currse,                    
                #     term=term,
                #     exam_type=ex.exam_type,
                #     session=currse,
                #     subject=subject,
                #     klass=student.admitted_class,
                #     id=dt.qstcode)


                selq = qstns.get(id=dt.qstcode)

                sek=selq.qstn   
                ans=tblans.objects.get(qstn=selq)
                ans=ans.ans
                b=ans
                # b=str(ans)
                try:
                    opti = tbloptions.objects.get(qstn=selq)
                except:
                    opti = tbloptioni.objects.get(qstn=selq)

                d=opti.a
                e=opti.b
                g=opti.c
                w=opti.d

                ##student ans = a, correct ans = b

                if a == b: # if my answer is correct
                    if ty=='update':
                        dt.score=1
                        dt.stu_ans=a
                        dt.save()


                    elif ty=='save':

                        try:
                            k=cbttrans.objects.get(student=student,
                                session=currse,
                                term=term,exam_type=ex.exam_type,
                                question=selq,
                                stu_ans=a,
                                score = 1,
                                no=number,
                                qstcode=selq.id,
                                subject=subject)
                        
                        except:

                            k=cbttrans(student=student,
                                session=currse,term=term,
                                exam_type=ex.exam_type,
                                question=selq,
                                stu_ans=a, score = 1, 
                                no=number,qstcode=selq.id,
                                subject=subject).save()
                
                else:#if my ans is wrong
                    if a == d or a == e or a == g or a == w:
                    # if a == str(d) or a == str(e) or a == str(g) or a == str(w):
                        if ty=='update':
                            dt.score=0
                            dt.stu_ans=a
                            dt.save()
                        elif ty=='save':

                            try:
                                cbttrans.objects.get(student=student,
                                    term=term,
                                    exam_type=ex.exam_type,
                                    question=selq,
                                    stu_ans=a,
                                    score = 0,
                                    no=number,
                                    status=0,
                                    qstcode=selq.id,
                                    subject=subject,
                                    session=currse)
                            except:

                                cbttrans(student=student,
                                    term=term,
                                    exam_type=ex.exam_type,
                                    question=selq,
                                    stu_ans=a,
                                    score = 0,
                                    no=number,
                                    status=0,
                                    qstcode=selq.id,
                                    subject=subject,
                                    session=currse).save()
                    else:
                        ty='whales'
                        tk = selq
                        ans=''
             
### porting to reportsheet module****************
                mycount = cbttrans.objects.filter(student=student,session=currse,
                        term=term, exam_type=ex.exam_type,
                        subject=subject)
                add=mycount.aggregate(Sum('score'))

                add = add['score__sum']

                

                acaderec = StudentAcademicRecord.objects.get(student = student, term=term)

                if ex.exam_type=='Mid term':
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                        subject=subject,term=term,session=currse).update(second_ca=add)
                elif ex.exam_type=='Ca 1':
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                        subject=subject,term=term,session=currse).update(first_ca=add)
                elif ex.exam_type=='Ca 2':
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                        subject=subject,term=term,session=currse).update(fourth_ca=add)
                elif ex.exam_type=='End term':
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                        subject=subject,term=term,session=currse).update(fifth_ca=add)

                if ty == 'save': #if i added a new entry to cbttrans

                    dt.delete()
                    count=mycount.count()+1
                    transid=[]
                    transid=[int(k.qstcode) for k in mycount]
                    

                    myq=[]
                    myq=[int(q.id) for q in qstns]

                    qu=[]            
                    qu= [item for item in myq  if item not in transid]

                    if qu == []:
                        # qc.delete()
                        # now_scheduled.delete()
                        # donsub=donesubjects(student=student,
                        #     exam_type=ex.exam_type, 
                        #     subject=subject, term=term,session=currse).save()
        
                        return render_to_response('CBT/done.html')

                    uid = 0
                    uid = random.choice(qu)
                    tk=0

                    # tk = tblquestion.objects.get(term=term, 
                    #         exam_type=ex.exam_type, 
                    #         session=currse,
                    #         subject=subject,
                    #         klass=student.admitted_class,
                    #         id=uid)

                    tk = qstns.get(id=uid)
                    
                    try:
                        cbtold.objects.get(session=currse,
                            question=tk,
                            term=term,
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject,
                            student=student,
                            qstcode=tk.id)
                    except:
                        cbtold(session=currse,
                                question=tk,
                                term=term,
                                exam_type=ex.exam_type,
                                klass=student.admitted_class,
                                subject=subject,
                                student=student,
                                qstcode=tk.id).save()

                        n2=number+1
                        qc.number=n2
                        qc.save()

                elif ty=='update':     #if i updated

                    n2=number+1
                    qc.number=n2
                    qc.save()  

                    try:

                        qs= cbttrans.objects.get(student=student,session=currse,
                            term=term,exam_type=ex.exam_type,no=n2,subject=subject)
                        ans=qs.stu_ans

                        # tk = tblquestion.objects.get(term=term, 
                        # exam_type=ex.exam_type, 
                        # session=currse,
                        # subject=subject,
                        # klass=student.admitted_class,

                        # id=qs.qstcode)

                        tk = qstns.get(id=qs.qstcode)
                        
                    except:

                        qs=cbtold.objects.get(student=student,
                            session=currse,
                            term=term,                            
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject)
                        ans=''

                        # tk = tblquestion.objects.get(term=term, 
                        # exam_type=ex.exam_type, 
                        # session=currse,
                        # subject=subject,
                        # klass=student.admitted_class,
                        # id=qs.qstcode)

                        tk = qstns.get(id=qs.qstcode)
                  
                if ty != 'whales':
                    number=number+1
            
            
            else: #if i didnt chose an option


                transid=[]
                transid=[int(k.qstcode) for k in mycount]

                myq=[]
                myq=[int(q.id) for q in qstns]

                qu=[]            
                qu= [item for item in myq  if item not in transid]

                if qu == []:
                    msg = number
                    if number < qcount:
                        qc.number=number+1
                        qc.save()
                        number=qc.number

                        qs = cbttrans.objects.get(student=student,session=currse,
                                term=term,exam_type=ex.exam_type,
                                no=number,subject=subject)

                        ans=qs.stu_ans

                        # tk = tblquestion.objects.get(term=term,
                        #         exam_type=ex.exam_type, 
                        #         session=currse,
                        #         subject=subject,
                        #         klass=student.admitted_class,
                        #         id=qs.qstcode)
                        tk = qstns.get(id=qs.qstcode)
                                    
                        k = tbloptions.objects.filter(qstn=tk).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=tk)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=tk)
                            image='low'
                        tk1 =tk.qstn
                        img =tk.image
                     
                        return render_to_response('CBT/previous.html',{'question':tk1,
                            'school':school,
                            'count':number,
                            'form':student,
                            'pos':image,
                            'ans':ans,
                            'image':img,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'options':opt,
                            'term':term,
                            'uid':tk.id,
                            'subject':subject})



                    else:
                        return render_to_response('CBT/done.html')



                try:
                    qs = cbttrans.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,no=number,subject=subject)
                    f='old'

                except:
                    qs=cbtold.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,klass=student.admitted_class,subject=subject)
                    ans=''
                    f= 'fresh'

                if f == 'old':
                    qc.number=number+1
                    qc.save()
                    number=qc.number
        
                    try:
                        qs = cbttrans.objects.get(student=student,session=currse,
                                term=term,exam_type=ex.exam_type,
                                no=number,subject=subject)

                        ans=qs.stu_ans

                        # tk = tblquestion.objects.get(term=term,
                        #         exam_type=ex.exam_type, 
                        #         session=currse,
                        #         subject=subject,
                        #         klass=student.admitted_class,
                        #         id=qs.qstcode)
                        tk = qstns.get(id=qs.qstcode)
                                    
                        k = tbloptions.objects.filter(qstn=tk).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=tk)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=tk)
                            image='low'
                        tk1 =tk.qstn
                        img =tk.image
                     
                        return render_to_response('CBT/previous.html',{'question':tk1,
                            'school':school,
                            'count':number,
                            'form':student,
                            'pos':image,
                            'ans':ans,
                            'image':img,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'options':opt,
                            'term':term,
                            'uid':tk.id,
                            'subject':subject})
                
                    except:
                        qs=cbtold.objects.get(student=student,session=currse,term=term,
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject)
                        ans=''      
                 
                        # tk = tblquestion.objects.get(term=term, 
                        #             exam_type=ex.exam_type, 
                        #             session=currse,
                        #             subject=subject,
                        #             klass=student.admitted_class,
                        #             id=qs.qstcode)

                        tk = qstns.get(id=qs.qstcode)
                    
                        k = tbloptions.objects.filter(qstn=tk).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=tk)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=tk)
                            image='low'
                        tk1 =tk.qstn
                        img =tk.image

                        return render_to_response('CBT/pupiltest.html',{'question':tk1,
                                    'school':school,
                                'count':number,
                                'form':student,
                                'pos':image,
                                'ans':ans,
                                'questioncount':qcount,
                                'image':img,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})

                elif f=='fresh':
                    # tk = tblquestion.objects.get(term=term,               
                    #         exam_type=ex.exam_type, 
                    #         session=currse,
                    #         subject=subject,
                    #         klass=student.admitted_class,
                    #         id=qs.qstcode)

                    tk = qstns.get(id=qs.qstcode)
        
                    k = tbloptions.objects.filter(qstn=tk).count()
                    if k == 0:
                        opt = tbloptioni.objects.filter(qstn=tk)
                        image='hi'
                    else:
                        opt = tbloptions.objects.filter(qstn=tk)
                        image='low'
                    tk1 =tk.qstn
                    img =tk.image
                    return render_to_response('CBT/pupiltest.html',{'question':tk1,
                                'school':school,'count':number,'form':student,'questioncount':qcount,
                                'pos':image,'ans':ans,'image':img,'session':currse,
                                'name':student.admissionno,'klass':student.admitted_class,
                                'adm':student.admissionno,'options':opt,
                                'term':term,'uid':tk.id,'subject':subject})

        
            k = tbloptions.objects.filter(qstn=tk).count()
            if k == 0:
                opt = tbloptioni.objects.filter(qstn=tk)
                image='hi'
            else:
                opt = tbloptions.objects.filter(qstn=tk)
                image='low'
            tk1 =tk.qstn
            img =tk.image

            return render_to_response('CBT/pupiltest.html',{'question':tk1,
                        'school':school,'count':number,'form':student,
                        'pos':image,'ans':ans,'image':img,'questioncount':qcount,
                        'session':currse,'name':student.admissionno,
                        'klass':student.admitted_class, 'adm':student.admissionno,
                        'options':opt,'term':term,'uid':tk.id,'subject':subject})
        else:
            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')



def next_original(request):
    if "userid" in request.session:        
        
        if request.method=='POST':
            varuser=request.session['userid']
            student=Student.objects.get(admitted_session=currse,admissionno=varuser,gone=False)
            
            ex=tblcbtexams.objects.get(status='ACTIVE')
            
            try:
                now_scheduled= scheduled.objects.get(student=student,
                    term=term,assessment=ex.exam_type,
                    session=currse)
                subject=now_scheduled.subject

            except:
                msg= 'SOMETHING WENT WRONG!!! CONTACT THE HEAD OF I.T'
                return render_to_response('CBT/nosub.html',{'varerr':msg})

            qstns=tblquestion.objects.filter(term=term,exam_type=ex.exam_type,
                session=currse,subject=subject,
                klass=student.admitted_class)
            qcount=qstns.count()


            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)
            number=int(qc.number)


            mycount = cbttrans.objects.filter(student=student,session=currse,
                    term=term, exam_type=ex.exam_type,
                    subject=subject)

#if i choose an answer
            if 'gender' in request.POST: #if option is selected
                a= request.POST['gender']
                    
                try:
                    dt = cbttrans.objects.get(student=student,session=currse,
                        term=term,exam_type=ex.exam_type,
                        no=number,subject=subject)
                    ty='update'
                except:                 
                    dt=cbtold.objects.get(student=student,session=currse,
                        term=term,exam_type=ex.exam_type,
                        klass=student.admitted_class,subject=subject)
                    ty='save'
                
                selq= tblquestion.objects.get(session=currse,
                    term=term,
                    exam_type=ex.exam_type,
                    klass=student.admitted_class,
                    subject= subject,
                    id=dt.qstcode)

                sek=selq.qstn   
                ans=tblans.objects.get(qstn=selq)
                ans=ans.ans
                b=str(ans)
                try:
                    opti = tbloptions.objects.get(qstn=selq)
                except:
                    opti = tbloptioni.objects.get(qstn=selq)

                d=opti.a
                e=opti.b
                g=opti.c
                w=opti.d

                ##student ans = a, correct ans = b

                if a == b: # if my answer is correct
                    if ty=='update':
                        dt.score=1
                        dt.stu_ans=a
                        dt.save()


                    elif ty=='save':

                        try:
                            k=cbttrans.objects.get(student=student,
                                session=currse,
                                term=term,exam_type=ex.exam_type,
                                question=selq,
                                stu_ans=a,
                                score = 1,
                                no=number,
                                qstcode=selq.id,
                                subject=subject)
                        
                        except:

                            k=cbttrans(student=student,
                                session=currse,term=term,
                                exam_type=ex.exam_type,
                                question=selq,
                                stu_ans=a, score = 1, 
                                no=number,qstcode=selq.id,
                                subject=subject).save()
                
                else:#if my ans is wrong
                   
                    if a == str(d) or a == str(e) or a == str(g) or a == str(w):
                        if ty=='update':
                            dt.score=0
                            dt.stu_ans=a
                            dt.save()
                        elif ty=='save':

                            try:
                                cbttrans.objects.get(student=student,
                                    term=term,
                                    exam_type=ex.exam_type,
                                    question=selq,
                                    stu_ans=a,
                                    score = 0,
                                    no=number,
                                    status=0,
                                    qstcode=selq.id,
                                    subject=subject,
                                    session=currse)
                            except:

                                cbttrans(student=student,
                                    term=term,
                                    exam_type=ex.exam_type,
                                    question=selq,
                                    stu_ans=a,
                                    score = 0,
                                    no=number,
                                    status=0,
                                    qstcode=selq.id,
                                    subject=subject,
                                    session=currse).save()
                    else:
                        ty='whales'
                        tk = selq
                        ans=''
             
### porting to reportsheet module****************
                # mycount = cbttrans.objects.filter(student=student,session=currse,
                #         term=term, exam_type=ex.exam_type,
                #         subject=subject)
                add=mycount.aggregate(Sum('score'))

                add = add['score__sum']

                

                # acaderec = StudentAcademicRecord.objects.get(student = student, term=term)

                # if ex.exam_type=='Mid term':
                #     subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                #         subject=subject,term=term,session=currse).update(second_ca=add)
                # elif ex.exam_type=='Ca 1':
                #     subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                #         subject=subject,term=term,session=currse).update(first_ca=add)
                # elif ex.exam_type=='Ca 2':
                #     subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                #         subject=subject,term=term,session=currse).update(fourth_ca=add)
                # elif ex.exam_type=='End term':
                #     subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                #         subject=subject,term=term,session=currse).update(fifth_ca=add)

                if ty == 'save': #if i added a new entry to cbttrans

                    dt.delete()
                    count=mycount.count()+1
                    transid=[]
                    transid=[int(k.qstcode) for k in mycount]
                    

                    myq=[]
                    myq=[int(q.id) for q in qstns]

                    qu=[]            
                    qu= [item for item in myq  if item not in transid]
                    if qu == []:
                        # qc.delete()
                        # now_scheduled.delete()
                        # donsub=donesubjects(student=student,
                        #     exam_type=ex.exam_type, 
                        #     subject=subject, term=term,session=currse).save()
        
                        return render_to_response('CBT/done.html')

                    uid = 0
                    uid = random.choice(qu)
                    tk=0                        
                    tk = tblquestion.objects.get(term=term, 
                            exam_type=ex.exam_type, 
                            session=currse,
                            subject=subject,
                            klass=student.admitted_class,
                            id=uid)
                    
                    try:
                        cbtold.objects.get(session=currse,
                            question=tk,
                            term=term,
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject,
                            student=student,
                            qstcode=tk.id)
                    except:
                        cbtold(session=currse,
                                question=tk,
                                term=term,
                                exam_type=ex.exam_type,
                                klass=student.admitted_class,
                                subject=subject,
                                student=student,
                                qstcode=tk.id).save()

                        n2=number+1
                        qc.number=n2
                        qc.save()

                elif ty=='update':     #if i updated

                    n2=number+1
                    qc.number=n2
                    qc.save()  

                    try:

                        qs= cbttrans.objects.get(student=student,session=currse,
                            term=term,exam_type=ex.exam_type,no=n2,subject=subject)
                        ans=qs.stu_ans

                        tk = tblquestion.objects.get(term=term, 
                        exam_type=ex.exam_type, 
                        session=currse,
                        subject=subject,
                        klass=student.admitted_class,
                        id=qs.qstcode)
                        
                    except:

                        qs=cbtold.objects.get(student=student,
                            session=currse,
                            term=term,                            
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject)
                        ans=''

                        tk = tblquestion.objects.get(term=term, 
                        exam_type=ex.exam_type, 
                        session=currse,
                        subject=subject,
                        klass=student.admitted_class,
                        id=qs.qstcode)
                  
                if ty != 'whales':
                    number=number+1
            
            
            else: #if i didnt chose an option


                transid=[]
                transid=[int(k.qstcode) for k in mycount]
                

                myq=[]
                myq=[int(q.id) for q in qstns]

                qu=[]            
                qu= [item for item in myq  if item not in transid]
                if qu == []:
                    # qc.delete()
                    # now_scheduled.delete()
                    # donsub=donesubjects(student=student,
                    #     exam_type=ex.exam_type, 
                    #     subject=subject, term=term,session=currse).save()
    
                    return render_to_response('CBT/done.html')



                try:
                    qs = cbttrans.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,no=number,subject=subject)
                    f='old'

                except:
                    qs=cbtold.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,klass=student.admitted_class,subject=subject)
                    ans=''
                    f= 'fresh'

                if f == 'old':
                    qc.number=number+1
                    qc.save()
                    number=qc.number
        
                    try:
                        qs = cbttrans.objects.get(student=student,session=currse,
                                term=term,exam_type=ex.exam_type,
                                no=number,subject=subject)

                        ans=qs.stu_ans

                        tk = tblquestion.objects.get(term=term,
                                exam_type=ex.exam_type, 
                                session=currse,
                                subject=subject,
                                klass=student.admitted_class,
                                id=qs.qstcode)
                                    
                        k = tbloptions.objects.filter(qstn=tk).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=tk)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=tk)
                            image='low'
                        tk1 =tk.qstn
                        img =tk.image
                     
                        return render_to_response('CBT/previous.html',{'question':tk1,
                            'school':school,
                            'count':number,
                            'form':student,
                            'pos':image,
                            'ans':ans,
                            'image':img,
                            'session':currse,
                            'name':student.admissionno,
                            'klass':student.admitted_class,
                            'adm':student.admissionno,
                            'options':opt,
                            'term':term,
                            'uid':tk.id,
                            'subject':subject})
                
                    except:
                        qs=cbtold.objects.get(student=student,session=currse,term=term,
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject)
                        ans=''      
                 
                        tk = tblquestion.objects.get(term=term, 
                                    exam_type=ex.exam_type, 
                                    session=currse,
                                    subject=subject,
                                    klass=student.admitted_class,
                                    id=qs.qstcode)
                    
                        k = tbloptions.objects.filter(qstn=tk).count()
                        if k == 0:
                            opt = tbloptioni.objects.filter(qstn=tk)
                            image='hi'
                        else:
                            opt = tbloptions.objects.filter(qstn=tk)
                            image='low'
                        tk1 =tk.qstn
                        img =tk.image

                        return render_to_response('CBT/pupiltest.html',{'question':tk1,
                                    'school':school,
                                'count':number,
                                'form':student,
                                'pos':image,
                                'ans':ans,
                                'questioncount':qcount,
                                'image':img,
                                'session':currse,
                                'name':student.admissionno,
                                'klass':student.admitted_class,
                                'adm':student.admissionno,
                                'options':opt,
                                'term':term,
                                'subject':subject})

                elif f=='fresh':
                    tk = tblquestion.objects.get(term=term,               
                            exam_type=ex.exam_type, 
                            session=currse,
                            subject=subject,
                            klass=student.admitted_class,
                            id=qs.qstcode)
        
                    k = tbloptions.objects.filter(qstn=tk).count()
                    if k == 0:
                        opt = tbloptioni.objects.filter(qstn=tk)
                        image='hi'
                    else:
                        opt = tbloptions.objects.filter(qstn=tk)
                        image='low'
                    tk1 =tk.qstn
                    img =tk.image
                    return render_to_response('CBT/pupiltest.html',{'question':tk1,
                                'school':school,'count':number,'form':student,'questioncount':qcount,
                                'pos':image,'ans':ans,'image':img,'session':currse,
                                'name':student.admissionno,'klass':student.admitted_class,
                                'adm':student.admissionno,'options':opt,
                                'term':term,'uid':tk.id,'subject':subject})

        
            k = tbloptions.objects.filter(qstn=tk).count()
            if k == 0:
                opt = tbloptioni.objects.filter(qstn=tk)
                image='hi'
            else:
                opt = tbloptions.objects.filter(qstn=tk)
                image='low'
            tk1 =tk.qstn
            img =tk.image

            return render_to_response('CBT/pupiltest.html',{'question':tk1,
                        'school':school,'count':number,'form':student,
                        'pos':image,'ans':ans,'image':img,'questioncount':qcount,
                        'session':currse,'name':student.admissionno,
                        'klass':student.admitted_class, 'adm':student.admissionno,
                        'options':opt,'term':term,'uid':tk.id,'subject':subject})
        else:
            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')




def textts(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblquestion.objects.get(id=vid)
            session=qst.session
            klass=qst.klass
            subject=qst.subject
            term=qst.term
            exam=qst.exam_type
            code=qst.id

            return HttpResponseRedirect('/cbt/input_text/%s/%s/%s/%s/%s/%s/'%(code,str(session).replace('/','k'),str(klass).replace(' ','m'),term,str(subject).replace(' ','w'),str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')


def save_text(request,code,session,klass,term,subject,exam):
    session = str(session).replace('k','/')
    klass = str(klass).replace('m',' ')
    subject = str(subject).replace('w',' ')
    exam = str(exam).replace('p',' ')

    if request.method == 'GET':
        getdetails=[]
        details = tblquestion.objects.get(id = code)
        try:
            options=tbloptions.objects.get(qstn=details)
        except:
            options=''
        try:
            answer= tblans.objects.get(qstn=details)

        except:
             answer=''
            
        dicdetails={'options':options,'question':details,'answer':answer}

        return render_to_response('CBT/enteropt.html',{'getdetails':dicdetails,})
    # return render_to_response('CBT/enteroption.html',{'getdetails':qst,'exam':exam,'session':session,'klass':klass,'term':term,'subject':subject})#'state':options})




def images(request,vid):
    if 'userid' in request.session:
        if request.method=='POST':
            qst=tblquestion.objects.get(id=vid)
            session=qst.session
            klass=qst.klass
            subject=qst.subject
            term=qst.term
            exam=qst.exam_type
            code=qst.id

            return HttpResponseRedirect('/cbt/input_images/%s/%s/%s/%s/%s/%s/'%(code,str(session).replace('/','k'),str(klass).replace(' ','m'),term,str(subject).replace(' ','w'),str(exam).replace(' ','p')))

    else:
        return HttpResponseRedirect ('/login')


def setass(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(email = varuser)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/cbt/access_denied/')

        t1=t2=t3=t4=[]

        t1=['Ca 2','Mid term','End Term']
        t2=['Ca 1','Mid term','End Term']
        t4=['Ca 2','Mid term','Ca 1']
        t3=['Ca 2','End Term','Ca 1']

        varerr = ""
        getdetails =""
        if request.method == 'POST':
            form =assessmentform(request.POST) # A form bound to the POST data
            if form.is_valid():
                assess = form.cleaned_data['assess']
                status = form.cleaned_data['status']
                if assess == 'Ca 1':
                    if status =='ACTIVE':
                        tblcbtexams.objects.filter(exam_type=assess).update(status=status)
                        for t in t1:
                            tblcbtexams.objects.filter(exam_type=t).update(status='INACTIVE')
                
                elif assess == 'Ca 2':
                    if status =='ACTIVE':
                        tblcbtexams.objects.filter(exam_type=assess).update(status=status)
                        for t in t2:
                            tblcbtexams.objects.filter(exam_type=t).update(status='INACTIVE')

                elif assess == 'End Term':
                    if status =='ACTIVE':
                        tr= tblcbtexams.objects.get(exam_type=assess)
                        tr.delete()
                        tblcbtexams(status=status,exam_type=assess).save()
                        for t in t4:
                            tblcbtexams.objects.filter(exam_type=t).update(status='INACTIVE')

                elif assess == 'Mid term':
                    if status =='ACTIVE':
                        tr= tblcbtexams.objects.get(exam_type=assess)
                        tr.delete()
                        tblcbtexams(status=status,exam_type=assess).save()
                        for t in t3:
                            tblcbtexams.objects.filter(exam_type=t).update(status='INACTIVE')

                return HttpResponseRedirect('/cbt/assessment/set/')
        else:
            form = assessmentform()
            getdetails = tblcbtexams.objects.all().order_by('status')
        return render_to_response('CBT/assessment.html',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')




def save_images(request,code,session,klass,term,subject,exam):
    session = str(session).replace('k','/')
    klass = str(klass).replace('m',' ')
    subject = str(subject).replace('w',' ')
    exam = str(exam).replace('p',' ')

    if request.method == 'GET':
        getdetails=[]
        details = tblquestion.objects.get(id = code)
        try:
            options=tbloptions.objects.get(qstn=details)
        except:
            options=''
        try:
            answer= tblans.objects.get(qstn=details)

        except:
             answer=''
            
        dicdetails={'options':options,'question':details,'answer':answer}

        return render_to_response('CBT/qstoptions.html',{'getdetails':dicdetails,'state':options})








def userlist(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,klass= acccode.split(':')
                myqst=[]
                myqst=tblcbtuser.objects.filter(session=session,klass=klass).order_by('subject')
                return render_to_response('CBT/cbtuser.html',{'myqst':myqst,'klass':klass,'session':session})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def userdelete(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    myqst=tblcbtuser.objects.get(id = acccode)
                    return render_to_response('CBT/userdel.html',{'user':myqst})
                
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')


def miscellenous(request):
    if  "userid" in request.session:
        if request.method=='POST':
            getstu = tblcbtuser.objects.get(id=vid)
            getstu.delete()
            return HttpResponseRedirect('/cbt/set_user/subject/')
        else:
            form = ""
        return render_to_response('CBT/misc.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def yesajax(request,vid):
    if  "userid" in request.session:
        if request.method=='POST':
            getstu = tblcbtuser.objects.get(id=vid)
            getstu.delete()
            return HttpResponseRedirect('/cbt/set_user/subject/')
    else:
        return HttpResponseRedirect('/login/')

def noajax(request):
    if  "userid" in request.session:
        if request.method=='POST':
            return HttpResponseRedirect('/cbt/set_user/subject/')        
    else:
        return HttpResponseRedirect('/login/')



def noscheajax(request):
    if  "userid" in request.session:
        if request.method=='POST':
            return HttpResponseRedirect('/cbt/schedulling/active/')        
    else:
        return HttpResponseRedirect('/login/')


def yessche(request,vid):
    if  "userid" in request.session:
        if request.method=='POST':
            getstu = tblcbtsubject.objects.get(id=vid)
            term=getstu.term

#########STUDENT LIST
            if term == 'First':
                stulist = Student.objects.filter(admitted_session= getstu.session, admitted_class=getstu.klass,
                    gone= False,first_term=True)
            if term == 'Second':
                stulist = Student.objects.filter(admitted_session=getstu.session, admitted_class=getstu.klass,
                    gone= False,second_term=True)
            if term == 'Third':
                stulist = Student.objects.filter(admitted_session=getstu.session, admitted_class=getstu.klass,
                    gone= False,third_term=True)

            mylist =[a.id for a in stulist]
            
            yess=[]
            for k in mylist:
                sched = scheduled.objects.filter(student=k,assessment=getstu.exam_type,subject=getstu.subject,term=getstu.term,session=getstu.session)
                if sched.count() > 0:
                    yess.append('a')

            if yess==[]:
                getstu.delete()
            return HttpResponseRedirect('/cbt/schedulling/active/')
    else:
        return HttpResponseRedirect('/login/')








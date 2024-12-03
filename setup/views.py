# Create your views here.

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from setup.forms import *
from setup.models import *
from sysadmin.models import *
from student.models import *
from reportsheet.models import *
from academics.models import *
import datetime
from datetime import date
import xlrd
import xlwt
from django.contrib.admin.views.decorators import staff_member_required

from platformowners.utils import *
from django.core.serializers.json import json




def welcome(request):
    if  "userid" in request.session:
        varuser=request.session['userid']

        user = ratifyuser(varuser)
        
        return render_to_response('setup/success1.html',{
            'varuser':user['varuser'],
            'company':user['company'],
            'pincode':user['pincode']}) 
    else:
        return HttpResponseRedirect('/login/')


def classarm(request):
    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:

            if request.method == 'POST':

                branch_code = request.POST['branch_code']
                stream = request.POST['stream']
                stream_code = request.POST['stream_code']
                room = request.POST['room']




                
                staff=tblstaff.objects.get(email=varuser,status=1)
                hh= tbluserprofile.objects.get(email=varuser,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)

                pstr= tblplatformstreams.objects.get(stream_code=stream_code)
                bstr = tblbusinessstream.objects.get(branch=branch,stream_alias=stream)

                psection_code= bstr.section.section.section_code
                psec= tblplatformsections.objects.get(section_code=psection_code)
                bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




                psubsection_code= bstr.subsection.subsection.subsection_code
                psubsec= tblplatformsubsections.objects.get(subsection_code=psubsection_code)
                bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)


                bstroom =tblbusinessstreamrooms.objects.filter(branch=branch,
                    section=bsec,subsection=bsubsec,stream=bstr,room=room,status=1)

                if bstroom.count() ==0:

                    tblbusinessstreamrooms(branch=branch,
                        section=bsec,subsection=bsubsec,stream=bstr,room=room,status=1).save()


                    return HttpResponseRedirect('/setup/class/')

                else:
                    varerr ='Class Already in Set Up'
                return render_to_response('setup/classrooms.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

            else:

                form = Classroomform()

                # return render_to_response('setup/class_and_arm.html',{'dashboard':dashboard,'form':form,'class':getdetails,'arm':getarm})

                return render_to_response('setup/classrooms.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')




def getsection(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                email = post['userid']

                kk = []
                sdic = {}

                staff=tblstaff.objects.get(email=email,status=1)
                hh= tbluserprofile.objects.get(email=email,status=1)

                branch_code=hh.branch.branch_code

               
                branch= tblbranch.objects.get(branch_code=branch_code)

                seccc= tblsectionmanager.objects.filter(branch=branch, staff=staff,status=1)


                for j in seccc: 
                    j = j.section.section.section + ":" + j.section.section.section_code
                    s = {j:j}
                    sdic.update(s)

                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def getsubsection(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                variables=post['userid']
                email,section,section_code = variables.split(':')#post['userid']

                kk = []
                sdic = {}

                staff=tblstaff.objects.get(email=email,status=1)
                hh= tbluserprofile.objects.get(email=email,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)

                psec=tblplatformsections.objects.get(section_code=section_code)
                bsec=tblbusinesssections.objects.get(branch=branch,section=psec)
                bsubsec= tblbusinesssubsections.objects.filter(branch=branch,section=bsec)


      
                for j in bsubsec: 
                    j = j.subsection.subsection + ":" + j.subsection.subsection_code
                    s = {j:j}
                    sdic.update(s)

                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')



def getstream(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                variables=post['userid']
                email,subsection,subsection_code = variables.split(':')#post['userid']

                kk = []
                sdic = {}

                staff=tblstaff.objects.get(email=email,status=1)
                hh= tbluserprofile.objects.get(email=email,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)

                psubsec=tblplatformsubsections.objects.get(subsection_code=subsection_code)
                psec_code=psubsec.section.section_code
                psec=tblplatformsections.objects.get(section_code=psec_code)


                bsec=tblbusinesssections.objects.get(branch=branch,section=psec)
                bsubsec= tblbusinesssubsections.objects.get(branch=branch,section=bsec,subsection=psubsec)

                pstr= tblplatformstreams.objects.filter(section=psec,subsection=psubsec)
                bstr =tblbusinessstream.objects.filter(branch=branch,section=bsec,subsection=bsubsec)


                if bstr.count() >0:  
                    for j in bstr: 
                        j = j.stream_alias + ":" + j.stream.stream_code
                        s = {j:j}
                        sdic.update(s)


                else:

                    for j in pstr: 
                        j = '-----' + ":" + '363607677'
                        s = {j:j}
                        sdic.update(s)

                klist = sdic.values()
                for p in klist:
                    kk.append(p)


                return HttpResponse(json.dumps(kk), mimetype='application/json')
            


            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')



def getstreamajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    admin_email,stream,stream_code= client.split(':')



                    if  stream == '-----':
                        msg = 'Stream Not set up'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


                    elif  stream_code == '-----':
                        msg = 'Select a section from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

                    
                    staff=tblstaff.objects.get(email=admin_email,status=1)
                    hh= tbluserprofile.objects.get(email=admin_email,status=1)

                    branch_code=hh.branch.branch_code               
                    branch= tblbranch.objects.get(branch_code=branch_code)

                    pstr= tblplatformstreams.objects.get(stream_code=stream_code)
                    bstr = tblbusinessstream.objects.get(branch=branch,stream_alias=stream)

                    psection_code= bstr.section.section.section_code
                    psec= tblplatformsections.objects.get(section_code=psection_code)
                    bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




                    psubsection_code= bstr.subsection.subsection.subsection_code
                    psubsec= tblplatformsubsections.objects.get(subsection_code=psubsection_code)
                    bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)


                    bstr =tblbusinessstreamrooms.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,stream=bstr,status=1)



                    return render_to_response('setup/classroom_ajax.html',{'branch_code':branch_code,
                        'pstream':pstr,
                        'sec':bstr,
                        'stream_code':stream_code,
                        'stream':stream
                        })



                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def popstreamajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']
                    # stream = post['stream']

                    stream_code,branch_code, stream= client.split(':')

                    
                    staff=tblstaff.objects.get(email=varuser,status=1)
                    hh= tbluserprofile.objects.get(email=varuser,status=1)

                    branch_code=hh.branch.branch_code               
                    branch= tblbranch.objects.get(branch_code=branch_code)

                    pstr= tblplatformstreams.objects.get(stream_code=stream_code)
                    bstr = tblbusinessstream.objects.get(branch=branch,stream_alias=stream)

                    psection_code= bstr.section.section.section_code
                    psec= tblplatformsections.objects.get(section_code=psection_code)
                    bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




                    psubsection_code= bstr.subsection.subsection.subsection_code
                    psubsec= tblplatformsubsections.objects.get(subsection_code=psubsection_code)
                    bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)


                    bstr =tblbusinessstreamrooms.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,stream=bstr,status=1)





                    ff=[]

                    if bstr.count() ==1 : 
                        dd = bstr.get()
                        alias=dd.room
                    else :
                        alias =1
                    s={'stream':pstr.stream, 'alias':alias, 'company':branch}

                    ff.append(s)

                    return render_to_response('setup/classroom_ajax2.html',{'branch_code':branch_code,
                        'getdetails':ff,
                        'pstream':pstr,
                        'sec':bstr,
                        'stream_code':stream_code,
                        'stream':stream
                        })


                    return render_to_response('platformadministrators/stream2.html',{'getdetails':ff,
                        'stream_code':stream_code, 'section_code':section_code,'subsection_code':subsection_code,'branch_code':branch_code})


                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def subject(request):

    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:

            if request.method == 'POST':

                dept_code = request.POST['dept_code']
                dept = request.POST['department']
                category = request.POST['category']
                subject = request.POST['subject']


                
                staff=tblstaff.objects.get(email=varuser,status=1)
                hh= tbluserprofile.objects.get(email=varuser,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)


                psubject= tblplatformsubjectdept.objects.get(dept_code=dept_code)

                bsubject = tblbusinesssubjectdept.objects.get(branch=branch,
                    department=psubject)

                bsec_code=bsubject.section.section.section_code
                psec= tblplatformsections.objects.get(section_code=bsec_code)
                bsec= tblbusinesssections.objects.get(branch=branch,section=psec)


                bsubsect_code=bsubject.subsection.subsection.subsection_code
                psubsec= tblplatformsubsections.objects.get(subsection_code=bsubsect_code)
                bsubsec=tblbusinesssubsections.objects.get(branch=branch,section=bsec,subsection=psubsec)
                




                bstroom =tblbusinesssubject.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,
                        category=category,department=bsubject, 
                        status=1)

                if bstroom.count() ==0:
                    subject_code=generate_code()

                    tblbusinesssubject(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,subject_code=subject_code,
                        category=category,department=bsubject, 
                        status=1).save()



                return HttpResponseRedirect('/setup/subject/')


            else:

                form = subjectform()

                return render_to_response('setup/mysubject.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def getdepartment(request):

    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                variables=post['userid']
                email,subsection,subsection_code = variables.split(':')#post['userid']

                kk = []
                sdic = {}

                staff=tblstaff.objects.get(email=email,status=1)
                hh= tbluserprofile.objects.get(email=email,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)

                psubsec=tblplatformsubsections.objects.get(subsection_code=subsection_code)
                psec_code=psubsec.section.section_code
                psec=tblplatformsections.objects.get(section_code=psec_code)


                bsec=tblbusinesssections.objects.get(branch=branch,section=psec)
                bsubsec= tblbusinesssubsections.objects.get(branch=branch,section=bsec,subsection=psubsec)

                # pstr= tblplatformstreams.objects.filter(section=psec,subsection=psubsec)
                bstr =tblbusinessstream.objects.filter(branch=branch,section=bsec,subsection=bsubsec)

      
                
                dept = tblplatformsubjectdept.objects.filter(section=psec,
                    status=1,
                    subsection=psubsec)


                d=[]
                for k in dept:
                    vv = tblbusinesssubjectdept.objects.filter(branch=branch,
                        section= bsec,
                        subsection=bsubsec,
                        department =k,
                        status= 1)

                    if vv.count() == 1:
                        vb=vv.get()
                        d.append(vb)


                for j in d:
                    j = j.department.dept + ":" + j.department.dept_code
                    s = {j:j}
                    sdic.update(s)

                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')


            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')




def getdeptajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    admin_email,department,dept_code= client.split(':')


                    if  admin_email == '-----':
                        msg = 'Select a school from the clients list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


                    elif  department == '-----':
                        msg = 'Select a location from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


                    elif  dept_code == '-----':
                        msg = 'Select a section from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

                    
                    staff=tblstaff.objects.get(email=admin_email,status=1)
                    hh= tbluserprofile.objects.get(email=admin_email,status=1)

                    branch_code=hh.branch.branch_code               
                    branch= tblbranch.objects.get(branch_code=branch_code)

                    pstr= tblplatformsubjectdept.objects.get(dept_code=dept_code)

                    bstr = tblbusinesssubjectdept.objects.get(branch=branch,department=pstr)



                    ddd = tblbusinesssubjectdept.objects.filter(branch=branch)


                    psection_code= bstr.section.section.section_code
                    psec= tblplatformsections.objects.get(section_code=psection_code)
                    bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




                    psubsection_code= bstr.subsection.subsection.subsection_code
                    psubsec= tblplatformsubsections.objects.get(subsection_code=psubsection_code)
                    bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)
                    


                    suball = []
                    for p in ddd:
                        g =tblbusinesssubject.objects.filter(branch=branch,
                            section=bsec,subsection=bsubsec,department=p)

                        
                        sbdic = {'category':p.department.dept,'subject':g}

                        suball.append(sbdic)


                    if bsubsec.subsection.subsection== 'Senior Secondary':

                        return render_to_response('setup/mysubject_ajax1.html',{'branch_code':branch_code,
                            'suball':suball,
                            'dept_code':dept_code,
                            'subsection':bsubsec,
                            'department':department
                            })
                    else:

                        return render_to_response('setup/mysubject_ajax.html',{'branch_code':branch_code,
                            'suball':suball,
                            'dept_code':dept_code,
                            'subsection':bsubsec,
                            'department':department
                            })


                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')






def affective(request):

    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:

            if request.method == 'POST':

                dept_code = request.POST['dept_code']
                dept = request.POST['department']
                category = request.POST['category']
                subject = request.POST['subject']


                
                staff=tblstaff.objects.get(email=varuser,status=1)
                hh= tbluserprofile.objects.get(email=varuser,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)


                psubject= tblplatformsubjectdept.objects.get(dept_code=dept_code)

                bsubject = tblbusinesssubjectdept.objects.get(branch=branch,
                    department=psubject)

                bsec_code=bsubject.section.section.section_code
                psec= tblplatformsections.objects.get(section_code=bsec_code)
                bsec= tblbusinesssections.objects.get(branch=branch,section=psec)


                bsubsect_code=bsubject.subsection.subsection.subsection_code
                psubsec= tblplatformsubsections.objects.get(subsection_code=bsubsect_code)
                bsubsec=tblbusinesssubsections.objects.get(branch=branch,section=bsec,subsection=psubsec)
                




                bstroom =tblbusinesssubject.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,
                        category=category,department=bsubject, 
                        status=1)

                if bstroom.count() ==0:
                    subject_code=generate_code()

                    tblbusinesssubject(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,subject_code=subject_code,
                        category=category,department=bsubject, 
                        status=1).save()



                return HttpResponseRedirect('/setup/subject/')


            else:

                form = affectiveform()

                return render_to_response('setup/affective.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def viewaffecajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:
                


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    email,section,section_code= client.split(':')



                    if  section == '-----':
                        msg = 'Select a section from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



                    psec= tblplatformsections.objects.get(section=section)

                    bbb =tblplatformsubsections.objects.filter( section=psec,status= 1 )

                    bsec=tblbusinesssections.objects.get(branch = user['branch'], section=psec)

                    
                    sec = tblbusinessaffective.objects.filter(
                                branch=user['branch'],
                                section=bsec,
                                status = 1 )


                    # schoolname=school.name
                    # addresssss=Address.address


                    return render_to_response('platformadministrators/affective1.html',{
                        # 'branch_code':branch_code,
                        'section_code':section_code,
                        # 'school':schoolname,
                        'sec':sec,
                        # 'address':addresssss
                        }
                        )

 
                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def psychomotoor(request):

    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:

            if request.method == 'POST':

                dept_code = request.POST['dept_code']
                dept = request.POST['department']
                category = request.POST['category']
                subject = request.POST['subject']


                
                staff=tblstaff.objects.get(email=varuser,status=1)
                hh= tbluserprofile.objects.get(email=varuser,status=1)

                branch_code=hh.branch.branch_code               
                branch= tblbranch.objects.get(branch_code=branch_code)


                psubject= tblplatformsubjectdept.objects.get(dept_code=dept_code)

                bsubject = tblbusinesssubjectdept.objects.get(branch=branch,
                    department=psubject)

                bsec_code=bsubject.section.section.section_code
                psec= tblplatformsections.objects.get(section_code=bsec_code)
                bsec= tblbusinesssections.objects.get(branch=branch,section=psec)


                bsubsect_code=bsubject.subsection.subsection.subsection_code
                psubsec= tblplatformsubsections.objects.get(subsection_code=bsubsect_code)
                bsubsec=tblbusinesssubsections.objects.get(branch=branch,section=bsec,subsection=psubsec)
                




                bstroom =tblbusinesssubject.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,
                        category=category,department=bsubject, 
                        status=1)

                if bstroom.count() ==0:
                    subject_code=generate_code()

                    tblbusinesssubject(branch=branch,
                        section=bsec,subsection=bsubsec,
                        subject=subject,subject_code=subject_code,
                        category=category,department=bsubject, 
                        status=1).save()



                return HttpResponseRedirect('/setup/subject/')


            else:

                form = affectiveform()

                return render_to_response('setup/psychomote.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')
        
def viewpsychoajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    email,section,section_code= client.split(':')


                    if  section == '-----':
                        msg = 'Select a section from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



                    psec= tblplatformsections.objects.get(section=section)

                    bbb =tblplatformsubsections.objects.filter( section=psec,status= 1 )

                    psec = tblplatformsections.objects.get(section_code=section_code)

                    bsec=tblbusinesssections.objects.get(branch=user['branch'],section=psec)

                    
                    sec = tblbusinesspsychomotive.objects.filter(
                        # platformowner=platformadmin,
                                branch=user['branch'],
                                section=bsec,
                                status = 1 )


                    # schoolname=school.name
                    # addresssss=Address.address


                    return render_to_response('platformadministrators/psycho1.html',{
                        # 'branch_code':branch_code,
                        'section_code':section_code,
                        # 'school':schoolname,
                        'sec':sec,
                        # 'address':addresssss
                        })



                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')

















def assessment(request):

    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:

            if request.method == 'POST':

                assessment = request.POST['assessment']
                obtainable = request.POST['obtainable']
                section_code = request.POST['section_code']
                reportsheet = request.POST['reportsheet']


                         
                branch= user['branch']



                psec= tblplatformsections.objects.get(section_code=section_code)
                bsec= tblbusinesssections.objects.get(branch=branch,section=psec)


 

                v=tblmidtermhighest.objects.filter(branch=branch,section=bsec,reportsheet=reportsheet)

                if v.count()==1:
                    tt=v.get()

                    gg= tblmidtermbreakdown.objects.filter(branch=branch,section=bsec,
                        term_highest=tt,assessment=assessment)
                    
                    if gg.count() ==0:
                        tblmidtermbreakdown(branch=branch,section=bsec,
                            term_highest=tt,assessment=assessment,max_score=obtainable).save()



                return HttpResponseRedirect('/setup/assessment/')


            else:

                form = affectiveform()

                return render_to_response('setup/assessment.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')
  

def viewgetassessmentajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    email,section,section_code, reporttype= client.split(':')


                    if  section == '-----':
                        msg = 'Select a section from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

                    if reporttype == '-----':
                        msg = 'Select a reportsheet from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


                    psec= tblplatformsections.objects.get(section=section)

                    bbb =tblplatformsubsections.objects.filter( section=psec,status= 1 )


                    bsec=tblbusinesssections.objects.get(branch=user['branch'],section=psec)

                    

                    bd = tblbusinessassessment.objects.filter(branch=user['branch'],section=bsec,reportsheet=reporttype)

                    return render_to_response('setup/assessment1.html',{
                        # 'branch_code':branch_code,
                        'section_code':section_code,
                        # 'school':schoolname,
                        'sec':bd,
                        'reportsheet':reporttype
                        # 'address':addresssss
                        })

# 'branch_code':branch_code,
# 'section_code':section_code,
# 'school':schoolname,
# 'sec':df,
# 'reportsheet':reportsheet,
# 'address':addresssss})


                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')




def gradings(request):
    if  "userid" in request.session:

        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['admin']:
            branch = user['branch']


            if request.method == 'POST':

                domain = request.POST['domain']
                subsection = request.POST['subsection']
                section = request.POST['section']
                remark = (request.POST['remark']).upper()


                psec= tblplatformsections.objects.get(section=section)
                bsec=tblbusinesssections.objects.get(branch=branch,section=psec)


                psubsec= tblplatformsubsections.objects.get(subsection=subsection)
                bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)



                if domain=='Cognitive':
                    fromm = request.POST['fromm']
                    tto = request.POST['tto']
                    grade = (request.POST['grade']).upper()

                    vrange = fromm + '-' + tto


                    bstroom =tblcognitivegrade.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,vrange=vrange)


                    if bstroom.count() ==0:
                        tblcognitivegrade(branch=branch,
                        section=bsec,subsection=bsubsec,
                        vrange=vrange,grade=grade,remark=remark).save()



                elif domain== 'Affective':
                    vrange = request.POST['vvalue']

                    bstroom =tblaffectivegrade.objects.filter(branch=branch,
                        section=bsec,subsection=bsubsec,vrange=vrange)


                    if bstroom.count() ==0:
                        tblaffectivegrade(branch=branch,
                        section=bsec,subsection=bsubsec,
                        vrange=vrange,remark=remark).save()

                
                return HttpResponseRedirect('/setup/grading/')


            else:

                form = gradingform()

                return render_to_response('setup/grading.html',{
                    'form':form,
                    'varuser':user['varuser'],
                    'company':user['company'],
                    'pincode':user['pincode']})        


        else:

            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')



def getgradeajax(request):
    if request.is_ajax():
        if  "userid" in request.session:
            varuser = request.session['userid']

            user = ratifyuser(varuser)

            if user['admin']:


                if request.method == 'POST':
                    post = request.POST.copy()
                    client = post['userid']

                    admin_email,subsection,subsection_code,domain= client.split(':')


                    if  subsection == '-----':
                        msg = 'Select a subsection from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


                    elif  domain == '-----':
                        msg = 'Select a domain from the list'
                        return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

                    


                    branch = user['branch']
                    psubsec= tblplatformsubsections.objects.get(subsection_code= subsection_code)
                    bsubsec=tblbusinesssubsections.objects.get(branch=branch,subsection=psubsec)

                    bsec2 = bsubsec.section.section.section
                    psec = tblplatformsections.objects.get(section=bsec2)
                    bsec=tblbusinesssections.objects.get(branch=branch,section=psec)



                    if domain =='Cognitive':

                        bstr =tblcognitivegrade.objects.filter(branch=branch,
                            section=bsec,subsection=bsubsec)

                        return render_to_response('setup/grading_ajax.html',{
                            'subsection':subsection,
                            'domain':domain,
                            'sec':bstr,
                            'section':bsec2
                            })


                    elif  domain == 'Affective':


                        bstr =tblaffectivegrade.objects.filter(branch=branch,
                            section=bsec,subsection=bsubsec)

                        return render_to_response('setup/grading_ajax2.html',{
                            'subsection':subsection,
                            'domain':domain,
                            'sec':bstr,
                            'section':bsec2,
                            # 'stream':stream
                            })


                else:
                    return HttpResponseRedirect('/login/')


            else:
                return HttpResponseRedirect('/login/')

        else:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')







def addarm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
   
        getdetails = Class.objects.all().order_by('klass')
        getarm = Arm.objects.all().order_by('arm')

        
        if request.method == 'POST':
            form2 = myarmform(request.POST) # A form bound to the POST data
            if form2.is_valid():
                arm = form2.cleaned_data['arm']
                klass = form2.cleaned_data['klass']

                kls =  Class.objects.get(klass=klass)

                if Arm.objects.filter(klass = kls, arm = arm.upper()).count() == 0:

                    try:
                        savecon = Arm(klass=kls, arm = arm.upper())
                        savecon.save()

                    except:
                        r=0

                    return HttpResponseRedirect('/setup/arm/')
                else:
                    varerr = 'Arm in Existence'
                    return render_to_response('setup/arm.html',{'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

        else:

            form2 = ClassForm2()

        return render_to_response('setup/arm.html',{'form2':form2,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')



def myclassroom(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                kls =  Class.objects.get(klass=acccode)
                aarm = Arm.objects.filter(klass=kls)

                return render_to_response('setup/classroom.html',{'getdetails':aarm,'klass':acccode})
                

            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')




def deleteclasscode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Class.objects.get(id = invid)
        k = getdetails.klass
        if Student.objects.filter(admitted_class = k ).count() == 0 :
            seldata = Class.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/class/')
        else:
            varerr = 'Students already in this class'
            form = ClassForm()
            form2 = ArmForm()
            getdetails = Class.objects.all().order_by('klass')
            getarm = Arm.objects.all().order_by('arm')
            return render_to_response('setup/class_and_arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def deletearmcode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Arm.objects.get(id = invid)
        k = getdetails.arm
        if Student.objects.filter(admitted_arm = k ).count() == 0 :
            seldata = Arm.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/arm/')
        else:
            varerr = 'Students already in this Arm'
            form = ClassForm()
            form2 = ArmForm()
            getdetails = Class.objects.all().order_by('klass')
            getarm = Arm.objects.all().order_by('arm')
            return render_to_response('setup/arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def subjecttt(request):
    if  "userid" in request.session:
         varuser = request.session['userid']
         user = tbluserprofile.objects.get(email = varuser)
         uenter = user.setup
         if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
         sublist = ['KG','Nursery','PRY','JS','Art','Science','Commercial','Science/Math','Technology']
         suball = []
         for p in sublist:
             subcat = Subject.objects.filter(category = p).order_by('subject')  #num is a count of similar entries in the db
             sbdic = {'category':p,'subject':subcat}
             suball.append(sbdic)
         varerr =''

         if request.method == 'POST':
            form = susesyform(request.POST) # A form bound to the POSTED data

            if form.is_valid():
                category = form.cleaned_data['category']
                group = form.cleaned_data['group']
                subj = form.cleaned_data['subject']


                subj = subj.upper()
                if Subject.objects.filter(subject=subj, category=category):
                    varerr = 'This Subject Already Exists!'
                    return render_to_response('setup/subjects1.html',{'form':form,'varerr':varerr})
                vcount = Subject.objects.filter(category=category).count()
                vcount1 = vcount + 1
                   #print vcount,vcount1
                savecon = Subject(status= 'INACTIVE',
                    category = category,
                    category2 = group,
                    subject = subj,
                    ca = 40,exam = 60,num = vcount1)
                savecon.save()
                return HttpResponseRedirect('/setup/subject/')

         else:
            form = susesyform()
         return render_to_response('setup/subjects1.html',{'varuser':varuser,'form':form,'suball':suball,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')





def subjectgroup(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.setup
        getdetails = Subject_group.objects.all().order_by('subject_group')
        getarm = Subject_group.objects.all().order_by('subject_group')
        if uenter is False :
           return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = subject_groupForm()
        if request.method == 'POST':
            form = subject_groupForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgroup = form.cleaned_data['subject_group']
                if Subject_group.objects.filter(subject_group = subgroup.upper()).count() == 0:
                   savecon = Subject_group(subject_group = subgroup.upper())
                   savecon.save()
                   return HttpResponseRedirect('/setup/subject_group/')
                else:
                    varerr = 'Arm in Existence'
                    return render_to_response('setup/subject_group.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

        else:
            form = subject_groupForm()

        return render_to_response('setup/subject_group.html',{'form':form,'varuser':varuser,'class':getdetails,'arm':getarm})
    else:
        return HttpResponseRedirect('/login/')


def deletesubjectgroupcode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Subject_group.objects.get(id = invid)
        k = getdetails.subject_group
        if SubjectScore.objects.filter(subject_group = k ).count() == 0 :
            seldata = Subject_group.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/subject_group/')
        else:
            varerr = 'Students already have this group'
            form = subject_groupForm()
            getarm = Subject_group.objects.all().order_by('id')
            return render_to_response('setup/subject_group.html',{'form':form,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def house(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        # uenter = user.setup
        # if uenter is False :
        #     return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = House.objects.all().order_by('house')
        if request.method == 'POST':
            form = HouseForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                house = form.cleaned_data['house']
                house = house.upper()
                if House.objects.filter(house=house):
                    varerr = 'This House Already Exists!'
                    return render_to_response('setup/schoolhouse.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
                savecon = House(house = house)
                savecon.save()
                return HttpResponseRedirect('/setup/schoolhouse/')
        else:
            form = HouseForm()
        return render_to_response('setup/schoolhouse.html',{'varuser':varuser,'form':form,'getdetails':getdetails,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def deletehousecode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = House.objects.get(id = invid)
        k = getdetails.house
        if Student.objects.filter(house = k ).count() == 0 :
            seldata = House.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/schoolhouse/')
        else:
            varerr = 'Students already given this house'
            getdetails = House.objects.all().order_by('house')
            form = HouseForm()
            return render_to_response('setup/schoolhouse.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def department(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        uenter = user.setup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = Department.objects.all().order_by('department')
        if request.method == 'POST':
            form = DepartmentForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                department = form.cleaned_data['department']
                department = department.upper()
                if Department.objects.filter(department=department):
                    varerr = 'This Department Already Exists!'
                    return render_to_response('setup/department_and_roles.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
                savecon = Department(department = department)
                savecon.save()
                return HttpResponseRedirect('/setup/departmentsandroles/')
        else:
            form = DepartmentForm()
        return render_to_response('setup/department_and_roles.html',{'form':form,'getdetails':getdetails,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')




def uploadlocalgovt(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluserprofile.objects.get(email = varuser)
        # uenter = user.editregistration
        # if uenter == False :
        #     return HttpResponseRedirect('/unauthorised/')
        varerr =''
        succ ="Select file"


        if request.method == 'POST':
            #row =""
            succ =""

            llgg = tblplatformlga.objects.all().count()

            if llgg == 0:

                if request.FILES['input_excel']:
                
                    input_excel=request.FILES['input_excel']
                    num = []
                    rows = "testing"
                    book = xlrd.open_workbook(file_contents=input_excel.read())
                    sheet = book.sheet_by_index(0)
                    for row_no in range(0, sheet.nrows):
                        rows = sheet.row_values(row_no)
                        num.append(rows)
                        #num = raw_str.split(",")
                    ncount = len(num)
                    # print raw_str
                    try:
                        for k in num:
                            j1 = k[0]
                            j2 = k[1]
                            savecon = tblplatformlga (state = j1,lga = j2)
                            savecon.save()
                        succ = "Record Uploaded !!!"
                        return render_to_response('setup/upload.html',{'succ':succ})
                    except:
                        succ ="Uploading Error "
                    return render_to_response('setup/upload.html',{'succ':succ})
            
        
            succ = "No file selected !!!"
            return render_to_response('setup/upload.html',{'succ':succ})
        

        else:
            return render_to_response('setup/upload.html', {'succ':succ})
    else:
        return HttpResponseRedirect('/login/')
# uploadlocal = staff_member_required(uploadlocal)






def uploadlocal(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    savecon = LGA (state = j1,lga = j2)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadlocal = staff_member_required(uploadlocal)

def getsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  Subject.objects.get(id = acccode)
                subjectlist = Subject.objects.all().order_by('num')
                fs = {}
                for k in subjectlist:
                    l = {k.category2:k.category2}
                    fs.update(l)
                nlist = fs.keys()
                return render_to_response('setup/getsubject.html',{'varuser':varuser,'subjectlist':nlist,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
#######UPDATE SUBJECT BUTTON ON edit subject dialog box in setup subject******************

def editsubject(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        if request.method == 'POST':
            sub = request.POST['subject']
            gid = request.POST['hcode']
            klass = request.POST['class']
            ca = request.POST['ca']
            exam = request.POST['exam']
            cate = request.POST['subjectlist']
            if ca == "" or exam == "" or klass == "" or "" :
                return HttpResponseRedirect('/setup/subject/')
            getdetails = Subject.objects.get(id = invid)
            if Subject.objects.filter(category = klass, subject = sub).exclude(id = invid).count() == 0:
                getdetails.category2 = cate
                getdetails.save()
                SubjectScore.objects.filter(session = currse,subject = gid).update(subject = sub)
                subjectteacher.objects.filter(subject = gid).update(subject = sub)
                return HttpResponseRedirect('/setup/subject/')
            else:
                return HttpResponseRedirect('/setup/subject/')

        else:
            return HttpResponseRedirect('/setup/subject/')
    else:
        return HttpResponseRedirect('/login/')


def uploadaccsubgrp(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                from ruffwal.rsetup.models import tblsubgroup
                for k in num:
                    j1 = k[0]#groupcode
                    j2 = k[1]#group name
                    j3 = k[2]#subcode
                    j4 = k[3]#sub name
                    j5 = k[4]#user id
                    savecon = tblsubgroup(groupname = str(j2),groupcode = str(j1),subgroupname =j4,subgroupcode = str(j3),userid = j5)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadaccsubgrp = staff_member_required(uploadaccsubgrp)

def uploadacc(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                from ruffwal.rsetup.models import tblaccount,tblsubgroup
                for k in num:
                    j1 = k[0]#accname
                    j2 = k[1]#acccode
                    j3 = k[2]#datecreated
                    j4 = k[3]#lasttrandate
                    j5 = k[4]#userid
                    j6 = k[5]#accbal
                    j7 = k[6]#accstatus
                    j8 = k[7]#groupname
                    j9 = k[8]#subgroupname
                    j10 = k[9]#recreport
                    j6_as_date = datetime.date(*xlrd.xldate_as_tuple(j3, 0)[:3])
                    j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j4, 0)[:3])
                    #print 'Datecreated ',j6_as_date,'Last trans date',j17_as_date
                    grc = tblsubgroup.objects.filter(groupname = j8)
                    subname = tblsubgroup.objects.filter(subgroupname = j9)
                    groupcode = ''
                    subgroupcode = ''
                    for j in grc:
                        groupcode =j.groupcode
                    for n in subname:
                        subgroupcode = n.subgroupcode

                    savecon = tblaccount(accname = j1,acccode = j2,accbal =j6,groupname = j8,groupcode = groupcode,datecreated = j6_as_date,subgroupname =j9,subgroupcode =subgroupcode,userid = j5,accstatus = j7,recreport = j10,lasttrandate = j17_as_date)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadacc = staff_member_required(uploadacc)

def uploadtransaction(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from ruffwal.rsetup.models import tblaccount,tblsubgroup
            from ruffwal.posting.models import tbltransaction
            for k in num:
                j1 = k[0]#acccode
                j2 = k[1]#transdate
                j3 = k[2]#cheque no
                j4 = k[3]#particular
                j5 = k[4]#credit
                j6 = k[5]#debit
                j7 = k[6]# balance
                j8 = k[7]#transmode
                j9 = k[8]#recdate
                j10 = k[9]#user id
                j11 = k[10]#trans id
                j2_as_date = datetime.date(*xlrd.xldate_as_tuple(j2, 0)[:3])
                #j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j4, 0)[:3])
                #print 'Last trans date',j2_as_date
                grc = tblaccount.objects.get(acccode = j1)
                savecon = tbltransaction(accname = grc.accname,acccode = j1,debit =j6,credit = j5,balance = j7,transid = str(j11),transdate =j2_as_date,particulars = j4,refno = j3,groupname = grc.groupname,subname = grc.subgroupname,userid = j10,recid = j11)
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
             #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadtransaction = staff_member_required(uploadtransaction)
def uploadstudent(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            #try:
            from ruffwal.rsetup.models import tblaccount
            for k in num:

                    surname = k[0]#transdate
                    firstname = k[1]#acccode
                    othername = k[2]#cheque no
                    address = k[3]#credit
                    sex = k[4]#debit
                    j2 = k[5]#particular
                    birth_place = k[6]# balance
                    state_of_origin = k[7]#transmode
                    lga = k[8]#recdate
                    studentpicture = k[9]#user id
                    fathername = k[10]#trans id
                    fatheraddress = k[11]#trans id
                    fathernumber = k[12]#trans id
                    fatheroccupation = k[13]#trans id
                    fatheremail = k[14]#trans id
                    prev_school = k[15]#trans id
                    prev_class = k[16]#trans id
                    admitted_class = k[17]#trans id
                    admitted_arm = k[18]#
                    admitted_session = k[19]#trans id
                    fullname = k[20]#trans id
                    admissionno = k[21]#trans id
                    house = k[22]#trans id
                    dayboarding = k[23]#trans id
                    varuser = k[24]#trans id
                    subclass = k[25]#trans id
                    newsession = '2013/2014'

                    birth_date = datetime.date(*xlrd.xldate_as_tuple(j2, 0)[:3])

                    submit = Student(birth_date= birth_date,admitted_session = admitted_session,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                    submit.save()
                    #********************************************************
                    submit1 = Student(birth_date= birth_date,admitted_session = newsession,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture =  studentpicture)
                    submit1.save()
                    fullname = str(surname) + ' ' + str(firstname) + ' '+ str(othername)
                    #used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                    #used.save()

            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
             #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadstudent = staff_member_required(uploadstudent)

def uploadbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from bill.models import tblbill

            for k in num:
                j1 = k[0]#class
                j2 = k[1]#desc
                j3 = k[2]#bill amount
                j4 = k[3]#acc code
                j5 = k[4]#day/boarding
                j6 = k[5]#term
                j7 = k[6]# userid
                savecon = tblbill(klass = str(j1),desc = str(j2),billamount =float(j3),acccode = str(j4),dayboarding = str(j5),term = str(j6),userid = str(j7))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbill = staff_member_required(uploadbill)



def uploadbillname(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from bill.models import tblexpenses

            for k in num:
                j1 = k[0]#class

                savecon = tblexpenses(name = str(j1))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbillname = staff_member_required(uploadbillname)

def uploadadditionalbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from bill.models import tbladditionalbill
            for k in num:
                j1 = k[0]#session
                j2 = k[1]#name
                j3 = k[2]#klass
                j4 = k[3]#term
                j5 = k[4]#bill amount
                j6 = k[5]#desc
                j7 = k[6]#acccode
                j8 = k[7]#user id
                if Student.objects.filter(fullname = j2):
                    admno = Student.objects.get(fullname = j2,admitted_session = '2012/2013').admissionno
                    arm = Student.objects.get(fullname = j2,admitted_session = '2012/2013').admitted_arm
                else:
                    admno = 'LC/0000000'
                    arm = 'A'
                savecon = tbladditionalbill(session = str(j1),admissionno = admno,name =str(j2),klass = str(j3),arm = arm,term = str(j4),billamount = float(j5),desc = str(j6),acccode = str(j7),userid = str(j8))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadadditionalbill = staff_member_required(uploadadditionalbill)

def uploadpostedbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from bill.models import postedbill
            for k in num:
                j1 = k[0]#session
                j2 = k[1]#klass
                j3 = k[2]#term
                j4 = k[3]#userid
                savecon = postedbill(session = str(j1),klass = str(j2),term =str(j3),userid = str(j4))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadpostedbill = staff_member_required(uploadpostedbill)


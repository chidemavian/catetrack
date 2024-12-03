from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse


from platformowners.utils import *
from sysadmin.models import *
from platformadministrators.forms import *

from django.core.serializers.json import json

from reportsheet.models import *
from setup.models import *

def homewelcome(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:

	        return render_to_response('platformadministrators/administratorsdashboard.html',
	            {'varuser':user['varuser'],
	            'company':user['company'],
	            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')




def newschool(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:
        	heading='Enter School Name'


        	if request.method=='POST':
        		platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        		school = request.POST['school']
        		website = request.POST['website']

        		reason= request.POST['reason']

        		business_type = tblplatformclient.objects.get(client_type=reason)

        		if 'colour' in request.FILES:
        			colour= request.FILES['colour']
        		else:
        			colour=''

        		if 'grey' in request.FILES:
        			grey= request.FILES['grey']
        		else:
        			grey=''

        		school_code=generate_code()

        		valid = tblschool.objects.filter(name=school)

        		if valid.count() >0:
        			r=0
        		else:

        			tblschool(platformadmin =platformadmin,
        					business_type=business_type,
							name =school,
							web = website,
							ig='',
							twitter = '',
							fb= '',
							youtube='',
							school_code= school_code,
							status= 1,
							logo_coloured = colour,
							logo_black = grey ).save()


		        return render_to_response('platformadministrators/successfull.html',
		            {'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})


        	else:

		        return render_to_response('platformadministrators/newschool.html',
		            {'heading':heading,
		             'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

    	else:
    		return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def editschool(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        valid = tbluserprofile.objects.get(email=user['varuser'])

        if valid.platformadmin == True:


        	if request.method=='POST':
        		H0=9



 # tblschool(
	# platformadmin =
	# name =
	# web = 
	# 	ig=
	# twitter = 
	# fb= 
	# youtube=
	# school_code=
	# status= 
	# logo_coloured = 

	# logo_black = 


        	else:


		        return render_to_response('platformadministrators/editschool.html',
		            {'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def newbranch(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        heading='Enter School Address'

        if user['pincode'].platformadmin == True:
        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':
        		address=request.POST['newaddress']
        		school_code=request.POST['school_code']
        		phone=request.POST['phone']
        		branch_code=generate_code()
        		school = tblschool.objects.get(school_code=school_code)

        		sc = tblbranch.objects.filter(company=school,address=address)

        		if sc.count() == 0:
        			tblbranch(company=school,address=address,branch_code=branch_code,phone=phone,status=1).save()

        		# branch = tblbranch.objects.get(branch_code=branch_code)

        		# tc = tblcurrentsession.objects


        		return render_to_response('platformadministrators/successfull.html')

        	else:
        		clients = tblschool.objects.filter(platformadmin=platformadmin).exclude(id=1)

		        return render_to_response('platformadministrators/newbranch.html',
		            {'heading':heading,
		            'data':clients,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def selectbranch(request):
    if request.is_ajax():


	    if  "userid" in request.session:
	        varuser = request.session['userid']

	        user = ratifyuser(varuser)


	    	if request.method == 'POST':
	    		post = request.POST.copy()
	    		client = post['userid']



	    		if  client == '-----':
	    			msg = 'Select a school from the clients list'
	    			return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

	    		else:

			        valid = tbluserprofile.objects.get(email=user['varuser'])

			        if valid.platformadmin == True:

			        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

			        	school = tblschool.objects.filter(school_code=client,platformadmin=platformadmin)
			        	dt=[]

			        	if school.count() ==1  :
			        		school=school.get()
		        			Address=tblbranch.objects.filter(company=school)
		        			details={'school':school,'Address':Address}
		        			dt.append(details)

			        		return render_to_response('platformadministrators/newbranch1.html',{'client':dt})

			        	else:
			    
			        		return HttpResponseRedirect('/login/')
			    	else:
			    		return HttpResponseRedirect('/login/')
	    	else:
	    		return HttpResponseRedirect('/login/')

	    else:
	    	return HttpResponseRedirect('/login/')

    else:
    	return HttpResponseRedirect('/login/')





def newsection(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:

	        heading='Enter Section'

        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':
        		section=request.POST['section']        		
    			branch_code=request.POST['branch_code']

    			if 'myselection' in request.POST:
    				myselection=request.POST['myselection']
    			else:
    				myselection=0

        		Address=tblbranch.objects.get(branch_code = branch_code)
        		ts = tblplatformsections.objects.get(section=section)


        		f= tblbusinesssections.objects.filter(branch=Address,section=ts)

        		if myselection == 'on':
        			if f.count() == 0:
        				tblbusinesssections(branch=Address,section=ts,status=1).save()
        		else:
        			if f.count() == 1:        				
	        			f=f.get()
	        			f.delete()

        		return render_to_response('platformadministrators/successfull.html')        	


        	else:
        		form = sectionform()    		

		        return render_to_response('platformadministrators/newsection.html',
		            {'heading':heading,
		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def getclient(request):
	if request.is_ajax():
		if  "userid" in request.session:

			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
				    varuser = request.session['userid']
				    varerr =""
				    post = request.POST.copy()
				    user = post['userid']
				    
				    kk = []
				    sdic = {}


				    platformadmin= tblplatformadministrators.objects.get(email=user)

				    data = tblschool.objects.filter(platformadmin=platformadmin).exclude(id=1)
				    for j in data:
				        j = j.name + ":" + j.school_code
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
	else:
	    return HttpResponseRedirect('/login/')


def getlocation(request):
	if request.is_ajax():
		if  "userid" in request.session:

			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:
				if request.method == 'POST':
					varuser = request.session['userid']
					varerr =""
					post = request.POST.copy()
					acccode = post['userid']

					user,name,school_code = acccode.split(':')
					kk = []
					sdic = {}

					platformadmin=tblplatformadministrators.objects.get(email=user)
					data = tblschool.objects.get(platformadmin=platformadmin, school_code=school_code)
					address= tblbranch.objects.filter(company=data)


					for j in address:
						j = j.address + ":" + j.branch_code
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
	else:
	    return HttpResponseRedirect('/login/')


def selectsection(request):
	if request.is_ajax():
		if  "userid" in request.session:

			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:
				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()

						client_type=school.business_type.client_type
						section_type= tblplatformclient.objects.get(client_type=client_type)


						Address=tblbranch.objects.get(branch_code = branch_code)

						platform_section=tblplatformsections.objects.filter(section_type=section_type)


						d=[]
						for k in platform_section:
							sec = tblbusinesssections.objects.filter(branch=Address,section=k,status=1)
							if sec.count() == 0 :
								alias=1
							elif sec.count() == 1:
								g=sec.get()
								alias='selected'

							s={'section':k.section,'alias':alias,'section_code':k.section_code}
							d.append(s)


						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/newsection111.html',{'branch_code':branch_code,
							'school':schoolname,
							'sec':d,
							'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')



def entersection(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)


			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				section_code,branch_code=bbb.split(":")

				
				if request.method == 'POST':		

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					Address=tblbranch.objects.get(branch_code = branch_code)


					my_section = tblplatformsections.objects.get(section_code=section_code)

					df = tblbusinesssections.objects.filter(branch=Address,section=my_section)
				
					if df.count()==0:
						du='unchecked'
					else:
						du='checked'


					schoolname=Address.company.name
					addresssss=Address.address

					return render_to_response('platformadministrators/newsection2.html',{'branch_code':branch_code,
						'school':schoolname,
						'sec':du,
						'section':my_section.section,
						'address':addresssss})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')




def savesection(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				section,branch_code= client.split(':')


				if  section == '-----':
					msg = 'Select a section from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					branch = tblbranch.objects.filter(branch_code=branch_code)
					dt=[]


					
					mysection = tblplatformsections.objects.get(section=section)
					g = tblbusinesssections.objects.filter(branch=branch,section=mysection)


					return render_to_response('platformadministrators/newsection1.html',{'branch_code':branch_code,'section':g,'act':section})

					
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')




def subsection(request):
    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:

	        heading='Enter Subsection'

	        platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        	if request.method=='POST':
        		subsection_code=request.POST['subsection']        		
    			branch_code=request.POST['branch_code']

    			if 'myselection' in request.POST:
    				myselection=request.POST['myselection']
    			else:
    				myselection=0

        		Address=tblbranch.objects.get(branch_code = branch_code)


        		ssub = tblplatformsubsections.objects.get(subsection_code= subsection_code)

        		sec7 = ssub.section.section
        		sec = tblplatformsections.objects.get(section=sec7)

        		bss= tblbusinesssections.objects.get(branch=Address,section=sec)

        		f= tblbusinesssubsections.objects.filter(branch=Address,subsection=ssub)



        		if myselection == 'on':
        			if f.count() == 0:
        				tblbusinesssubsections(branch=Address,section=bss,subsection= ssub, status=1).save()
        		else:
        			if f.count() == 1:        				
	        			f=f.get()
	        			f.delete()

        		return render_to_response('platformadministrators/successfull.html')         	

        	else:
        		form = subsectionform()    		

		        return render_to_response('platformadministrators/subsection.html',
		            {'heading':heading,		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def popsub(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				section_name,branch_code= client.split(':')


				if  section_name == '-----':
					msg = section_name
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					branch = tblbranch.objects.filter(branch_code=branch_code)
										
					# mysection = tblplatformsections.objects.get(section=section_name)
					mysection = tblplatformsubsections.objects.get(subsection=section_name)
					# d = tblbusinesssections.objects.get(branch=branch,section=mysection)
					g= tblbusinesssubsections.objects.filter(branch=branch,subsection=mysection)


					return render_to_response('platformadministrators/subsection3.html',
						{'branch_code':branch_code,
						'section':g,'act':section_name})

					
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')


def getsection(request):

    if  "userid" in request.session:
        if request.is_ajax():
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				user,name,school_code = acccode.split(':')
				kk = []
				sdic = {}

				platformadmin=tblplatformadministrators.objects.get(email=user)
				data = tblschool.objects.get(platformadmin=platformadmin, school_code=school_code)
				address= tblbranch.objects.get(company=data)

				seccc= tblbusinesssections.objects.filter(branch=address)


				if seccc.count() >0:
					for j in seccc:
						j = j.section.section + ":" + j.section.section_code
						s = {j:j}
						sdic.update(s)

					klist = sdic.values()
					for p in klist:
						kk.append(p)
				else:

					j = '-----' + ":" + '658658876'
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




def getsubsection(request):

    if  "userid" in request.session:
        if request.is_ajax():
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				user,branch,branch_code,section,section_code = acccode.split(':')

				kk = []
				sdic = {}


				if  section == '-----':

					j = '-----' + ":" + '999658876'
					s = {j:j}
					sdic.update(s)


					klist = sdic.values()
					for p in klist:
						kk.append(p)



				else:

					platformadmin=tblplatformadministrators.objects.get(email=user)

					address= tblbranch.objects.get(branch_code=branch_code)

					dc = tblplatformsections.objects.get(section_code=section_code)
					fd = tblbusinesssections.objects.get(branch=address, section=dc)

					seccc= tblbusinesssubsections.objects.filter(branch=address,section =fd )
					
					
					if seccc.count() >0:
						for j in seccc:
							j = j.subsection.subsection + ":" + j.subsection.subsection_code
							s = {j:j}
							sdic.update(s)

						klist = sdic.values()
						for p in klist:
							kk.append(p)

					else:

						j = '-----' + ":" + '999658876'
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


def subsectview(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


			
					elif  section == '-----':
						msg = 'No Section Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						psec= tblplatformsections.objects.get(section=section)

						bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

						d=[]
						for k in bbb:
						    sec = tblbusinesssubsections.objects.filter(branch=Address,subsection=k,status=1)
						    if sec.count() == 0 :
						        alias=1
						    elif sec.count() == 1:
						        g=sec.get()
						        alias='selected'

						    s={'subsection':k.subsection,'alias':alias,'subsection_code':k.subsection_code}
						    d.append(s)


						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/subsection1.html',{'branch_code':branch_code,
						    'school':schoolname,
						    'sec':d,
						    'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')


			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')




def subsec(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)


			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				subsection_code,branch_code=bbb.split(":")

				
				if request.method == 'POST':		

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					Address=tblbranch.objects.get(branch_code = branch_code)


					my_subsection = tblplatformsubsections.objects.get(subsection_code=subsection_code)
					sss= my_subsection.section.section

					df = tblbusinesssubsections.objects.filter(branch=Address,subsection=my_subsection)
				
					if df.count()==0:
						du='unchecked'
						state='Activate'
					else:
						du='checked'
						state='Deactivate'


					return render_to_response('platformadministrators/subsection2.html',{'branch_code':branch_code,
						'school':Address,
						'sec':du,
						'subsection_code':subsection_code,
						'section':sss,
						'state':state,
						'subsection':my_subsection.subsection})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')



def termnames(request):
    if  "userid" in request.session:
		varuser = request.session['userid']

		user = ratifyuser(varuser)


		heading='Set Term Alias'

		if user['pincode'].platformadmin == True:
			platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

			if request.method=='POST':
				school_code=request.POST['school_code']
				term_code=request.POST['term_code']
				term_alias=request.POST['myterm']

				school = tblschool.objects.get(school_code=school_code) 
				tt = tblplatformterms.objects.get(term_code = term_code)

				h= tblbusinessterms.objects.filter(school=school,term = tt)

				if h.count() == 1:
					h.update(term_alias=term_alias)
				elif h.count() ==0:
					tblbusinessterms(school=school,term = tt,term_alias= term_alias,systemadmin=platformadmin).save()

				return render_to_response('platformadministrators/successfull.html')

			else:
				form = schoolform()

			return render_to_response('platformadministrators/termname.html',
			    {'heading':heading,
			    'form':form,
			    'varuser':user['varuser'],
			    'company':user['company'],
			    'pincode':user['pincode']})

		else:
			return HttpResponseRedirect('/login/')
  
    else:
        return HttpResponseRedirect('/login/')


def settermname(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if  user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  school_code == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()

						if school.business_type.id == 1: #

							bbb =tblplatformterms.objects.all()
							d=[]
							for k in bbb:
							    sec = tblbusinessterms.objects.filter(school=school, term=k)

							    if sec.count() == 0 :
							        alias=1
							    elif sec.count() == 1:
							        g=sec.get()
							        alias=g.term_alias

							    s={'term':k.term,'alias':alias,'term_code':k.term_code}
							    d.append(s)

							return render_to_response('platformadministrators/termname1.html',{'school':school,
							    'sec':d,'school_code':school_code })

						elif school.business_type.id == 2:
							return render_to_response('platformadministrators/termname3.html')



					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')

			else:
				return HttpResponseRedirect('/login/')
		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')



def termpop(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']
			user = ratifyuser(varuser)
			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				term_code,school_code=bbb.split(":")
				
				if request.method == 'POST':		

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					myschool=tblschool.objects.get(school_code = school_code)

					term=tblplatformterms.objects.get(term_code=term_code)
	

					df = tblbusinessterms.objects.filter(school=myschool,term= term)
				
					if df.count()==0:
						alias=0
					else:
						df =df.get()
						alias = df.term_alias
				
					return render_to_response('platformadministrators/termname2.html',{'school_code':school_code,
						'school':myschool,
						'sec':alias,
						'term_code':term_code,
						'term': term.term})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')


def setapp(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:


        	heading='Activate Apps'


        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':

        		app_code=request.POST['app_code']        		
    			branch_code=request.POST['branch_code']
    			section=request.POST['section']

    			if 'myselection' in request.POST:
    				myselection=request.POST['myselection']
    			else:
    				myselection=0

        		Address=tblbranch.objects.get(branch_code = branch_code)


        		app = tblplatformapps.objects.get(app_code=app_code)

        		sec = tblplatformsections.objects.get(section=section)

        		bss= tblbusinesssections.objects.get(branch=Address,section=sec)

        		f= tblbusinessapp.objects.filter(branch=Address,section=bss,app=app)



        		if myselection == 'on':
        			if f.count() == 0:
        				tblbusinessapp(branch=Address,systemadmin=platformadmin, section=bss,app=app).save()
        		else:
        			if f.count() == 1:        				
	        			f=f.get()
	        			f.delete()

        		return render_to_response('platformadministrators/successfull.html') 

        	else:
        		form = selectappform()   		

		        return render_to_response('platformadministrators/app.html',
		            {'heading':heading,		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def selectapp(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if  user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'No Section Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



					elif  subsection == '-----':
						msg = 'No Subsection Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})



					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)

						bbb =tblplatformapps.objects.filter(status=1)
						ss = tblplatformsections.objects.get(section_code=section_code)
						bss = tblbusinesssections.objects.get(branch=Address, section=ss)


						d=[]
						for k in bbb:
						    sec = tblbusinessapp.objects.filter(branch=Address, section=bss,app=k)

						    if sec.count() == 0 :
						        alias=1
						    elif sec.count() == 1:
						        g=sec.get()
						        alias='selected'

						    s={'app':k.app,'alias':alias,'app_code':k.app_code}
						    d.append(s)


						return render_to_response('platformadministrators/app1.html',{'branch_code':branch_code,
						    'school':Address,
						    'sec':d,
						    'section':section })


					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')

			else:
				return HttpResponseRedirect('/login/')
		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






def sectionapp(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)


			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				app_code,branch_code,section=bbb.split(":")

				
				if request.method == 'POST':		

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					Address=tblbranch.objects.get(branch_code = branch_code)


					pltfm_app = tblplatformapps.objects.get(app_code=app_code)

					app=pltfm_app.app

					secc = tblplatformsections.objects.get(section=section)
					bss=tblbusinesssections.objects.get(branch=Address,section=secc)

	

					df = tblbusinessapp.objects.filter(branch=Address,section=bss,app=pltfm_app)
				
					if df.count()==0:
						du='unchecked'
						state = 'Activate'
					else:
						du='checked'
						state = 'Deactivate'



					return render_to_response('platformadministrators/app2.html',{'branch_code':branch_code,
						'school':Address,
						'sec':du,
						'app_code':app_code,
						'app':app,
						'section':section,
						'state': state})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






def subjects(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        valid = tbluserprofile.objects.get(email=user['varuser'])

        heading='Enter Subjects'

        if valid.platformadmin == True:
        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':



        		branch_code=request.POST['branch_code']

        		Address=tblbranch.objects.get(branch_code = branch_code)



        		return render_to_response('platformadministrators/successfull.html')        	

        	else:
        		form = sectionform()        		

		        return render_to_response('platformadministrators/subjectsections.html',
		            {'heading':heading,		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def selectsubject(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				name,school_code, address,branch_code,section= client.split(':')




				if  name == '-----':
					msg = 'Select a school from the clients list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  address == '-----':
					msg = 'Select a location from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

				else:
					valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						return render_to_response('platformadministrators/subjectsections1.html',{'sections':sub,
							'branch_code':branch_code,
							'sec':section})

					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')





def newadmin(request):


	if  "userid" in request.session:
		varuser = request.session['userid']

		user = ratifyuser(varuser)

		valid = tbluserprofile.objects.get(email=user['varuser'])

		heading='Register Admin User'

		if valid.platformadmin == True:
			platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])
			platformowner_code=platformadmin.platformowner.platformowners_code

			platformowner=tblplatformowners.objects.get(platformowners_code=platformowner_code)


			if request.method=='POST':

				surname=request.POST['surname']
				firstname=request.POST['firstname']
				othername=request.POST['othername']
				phone=request.POST['phone']
				photo=request.POST['photo']
				email=request.POST['email']

				section = request.POST['section']

				branch_code=request.POST['branch']

				pltsec= tblplatformsections.objects.get(section=section)
				

				Address=tblbranch.objects.get(branch_code = branch_code)

				business_section=tblbusinesssections.objects.get(branch = Address, section=pltsec)

				stf = tblstaff.objects.filter(email=email,status=1)

				staff_code=generate_code()
				manager_code=generate_code()
				password=generate_code()

				if stf.count() == 0:
					k='ok'
					
					# tblstaff(branch=Address,surname=surname,firstname=firstname,
					# 	othername=othername,email=email,
					# 	phone=phone,photo=photo,staff_code=staff_code,status=1).save()
				else:
					stf.update(status=0)

				tblstaff(branch=Address,surname=surname,firstname=firstname,
					othername=othername,email=email,
					phone=phone,photo=photo,staff_code=staff_code,status=1).save()




				stm = tblstaff.objects.filter(branch=Address,email=email,status=1)

				if stm.count() ==1: 
					staff=stm.get()
					fd = tblsectionmanager.objects.filter(branch=Address,section=business_section)

					if fd.count()==0:
						tblsectionmanager(branch=Address,staff=staff,section=business_section, 
							platformowner=platformowner, 
							manager_code=manager_code,status=1).save()


				uuser = tbluserprofile.objects.filter(branch=Address,
					    email = email,status=1,
					    staffrec=staff)

				if uuser.count() ==0:
				    tbluserprofile(branch=Address, platformownwer = 0,        				
						    platformadmin = 0,
						    email = email,
						    password = password,
						    staffrec=staff,
						    status = 1).save()

				else:
					msg='E-mail active somewhere else'
				 	return render_to_response('platformadministrators/successfull.html',{'msg':msg})




				msg = 'Admin user created'
				return render_to_response('platformadministrators/successfull.html',{'msg':msg})
			

			else:
				form = sectionform()        		

		        return render_to_response('platformadministrators/schooladmin.html',
		            {'heading':heading,		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

	else:

		return HttpResponseRedirect('/login/')
      



def setadmin(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				name,school_code, address,branch_code,section,section_code= client.split(':')




				if  name == '-----':
					msg = 'Select a school from the clients list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  address == '-----':
					msg = 'Select a location from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

				else:
					valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)
						platform_section=tblplatformsections.objects.get(section=section)

						busi_section = tblbusinesssections.objects.get(branch=Address,section=platform_section)

						bn = tblsectionmanager.objects.filter(branch=Address,section= busi_section)

						if bn.count() == 0 : 

							return render_to_response('platformadministrators/createwallet.html',{'branch_code':branch_code,
								'sec':section})

						else:


							return render_to_response('platformadministrators/schooladmin1.html',{'manager':bn,
								'branch_code':branch_code,
								'sec':section})

					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')

		



def reportsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:

	        heading='Set Reportsheet values'

	        platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        	if request.method=='POST':
				section_code=request.POST['section_code']        		
				branch_code=request.POST['branch_code']
				reportsheet=request.POST['reportsheet']
				highest_score=request.POST['highest_score']


				affective_code= generate_code()


				branch =tblbranch.objects.get(branch_code = branch_code)


				psec= tblplatformsections.objects.get(section_code=section_code)

				bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

				psec = tblplatformsections.objects.get(section_code=section_code)

				bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




				f =tblmidtermhighest.objects.filter(branch=branch,
					section=bsec,
					reportsheet = reportsheet,
					highest_score = highest_score)
				if f.count() ==0 :
			

					f =tblmidtermhighest(branch=branch,
						section=bsec,
						reportsheet = reportsheet,
						highest_score = highest_score).save()



				return render_to_response('platformadministrators/successfull.html')         	

        	else:
				form = subsectionform()    		

				return render_to_response('platformadministrators/reportsheet.html',
				    {'heading':heading,
				   
				    'form':form,
				    'varuser':user['varuser'],
				    'company':user['company'],
				    'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')

def reportsheetajax(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code,reportsheet= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Select a section from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  reportsheet == '-----':
						msg = 'Select reportsheet from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						psec= tblplatformsections.objects.get(section=section)

						bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

						psec = tblplatformsections.objects.get(section_code=section_code)

						bsec=tblbusinesssections.objects.get(branch=Address,section=psec)

						df = tblmidtermhighest.objects.filter(branch=Address,section=bsec,reportsheet=reportsheet)
						if df.count()==0:
							df=0
						elif df.count() ==1:
							df=df.get()


						# return render_to_response('platformadministrators/selectloan.html',{'msg':df})



						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/reportsheet1.html',{'branch_code':branch_code,
						    'section_code':section_code,
						    'school':schoolname,
						    'sec':df,
						    'reportsheet':reportsheet,
						    'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')

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

        if user['pincode'].platformadmin == True:

	        heading='Set Assessments'

	        platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        	if request.method=='POST':
				section_code=request.POST['section_code']        		
				branch_code=request.POST['branch_code']
				reportsheet=request.POST['reportsheet']
				assessment=request.POST['assessment']
				obtainable=request.POST['obtainable']


				

				branch =tblbranch.objects.get(branch_code = branch_code)


				psec= tblplatformsections.objects.get(section_code=section_code)


				bsec=tblbusinesssections.objects.get(branch=branch,section=psec)


				f =tblbusinessassessment.objects.filter(branch=branch,
					section=bsec,
					reportsheet = reportsheet,
					assessment = assessment)
				
				if f.count() ==0 :
			

					f =tblbusinessassessment(branch=branch,
						section=bsec,
						reportsheet = reportsheet,
						assessment = assessment,
						max_in= obtainable,
						assessment_status = 1).save()



				return render_to_response('platformadministrators/successfull.html')         	

        	else:
				form = subsectionform()    		

				return render_to_response('platformadministrators/assessment.html',
				    {'heading':heading,
				   
				    'form':form,
				    'varuser':user['varuser'],
				    'company':user['company'],
				    'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def assessementajax(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code,reportsheet= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Select a section from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  reportsheet == '-----':
						msg = 'Select reportsheet from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						psec= tblplatformsections.objects.get(section=section)

						# bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

						bsec=tblbusinesssections.objects.get(branch=Address,section=psec)

						df = tblbusinessassessment.objects.filter(branch=Address,section=bsec,reportsheet=reportsheet)



						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/assessment1.html',{
							'branch_code':branch_code,
						    'section_code':section_code,
						    'school':schoolname,
						    'sec':df,
						    'reportsheet':reportsheet,
						    'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')


			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')

def streamm(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        heading='Enter Stream'

        if user['pincode'].platformadmin == True:

        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':

				branch_code=request.POST['branch_code']
				stream_code=request.POST['stream_code']
				mystream=request.POST['mystream']
				subsection_code=request.POST['subsection_code']
				section_code=request.POST['section_code']
				

				branch =tblbranch.objects.get(branch_code = branch_code)

				ts = tblplatformstreams.objects.get(stream_code=stream_code)
				platformsub = tblplatformsubsections.objects.get(subsection_code=subsection_code)
				
				psec = tblplatformsections.objects.get(section_code=section_code)

				bsec = tblbusinesssections.objects.get(branch=branch,section=psec)

				
				business_stream = tblbusinessstream.objects.filter(branch=branch,section=bsec, stream=ts)

				bssub =  tblbusinesssubsections.objects.get(branch=branch,
					section=bsec,
					subsection=platformsub)


				if business_stream.count() == 0:
					tblbusinessstream(branch=branch,
						section= bsec,
						stream=ts,
						subsection= bssub,
						stream_alias = mystream,
						status= 1 ).save()

				elif business_stream.count() ==1:
					business_stream.update(stream_alias = mystream)



				return render_to_response('platformadministrators/successfull.html')        	

        	else:
        		form = streamform()    		

		        return render_to_response('platformadministrators/stream.html',
		            {'heading':heading,
		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def streamviw(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:

				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code,subsection,subsection_code= client.split(':')



					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Section not Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  subsection == '-----':
						msg = 'Subsection not Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)

						psec= tblplatformsections.objects.get(section=section)
						plsub = tblplatformsubsections.objects.get(subsection_code=subsection_code)						
						

						bsec = tblbusinesssections.objects.get(branch=Address,section=psec)
						bss = tblbusinesssubsections.objects.get(branch=Address,section=bsec, subsection=plsub)
						
						# d = tblbusinessstream.objects.get(branch=Address,status= 1,subsection=bss)

						# msg = {'section':bsec.section.section, 'sub-section':d.subsection.subsection.subsection}
						# return render_to_response('platformadministrators/selectloan.html',{'msg':msg})

						platformstream = tblplatformstreams.objects.filter(section=psec,status=1,subsection=plsub)

						d=[]
						for k in platformstream :
							vv = tblbusinessstream.objects.filter(branch=Address,section= bsec,subsection=bss, stream =k, status= 1)
							if vv.count() == 0:
								bb={'stream':k.stream,'alias':'Enter stream Alias','code':k.stream_code}
							elif vv.count() ==1:
								vb=vv.get()
								bb ={'stream':k.stream,'alias':vb.stream_alias,'code':k.stream_code}
							d.append(bb)



						return render_to_response('platformadministrators/stream1.html',{'branch_code':branch_code,	
									'business_streams':d,'section_code':section_code,
									'bsubsection':subsection_code})

					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')

			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')




def popstreamm(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
					varuser = request.session['userid']
					user = ratifyuser(varuser)  #ON BEHALF OF

					if user['pincode'].platformadmin == True:
						post = request.POST.copy()
						code = post['userid']
						stream_code,branch_code,subsection_code, section_code = code.split(':')

						branch=tblbranch.objects.get(branch_code=branch_code)
						psec=tblplatformsections.objects.get(section_code=section_code)
						pstream = tblplatformstreams.objects.get(stream_code=stream_code)						
						psub = tblplatformsubsections.objects.get(subsection_code=subsection_code)

						bsec = tblbusinesssections.objects.get(branch=branch,section=psec)
						bsub = tblbusinesssubsections.objects.get(branch=branch,section=bsec, subsection=psub)
						st = tblbusinessstream.objects.filter(stream=pstream,subsection=bsub,section=bsec)
						

						ff=[]

						if st.count() ==1 : 
							dd = st.get()
							alias=dd.stream_alias
						else :
							alias =1
						s={'stream':pstream.stream, 'alias':alias, 'company':branch}

						ff.append(s)
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







def department(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        heading='Activate Departments'

        if user['pincode'].platformadmin == True:

        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':

        		dept_code=request.POST['dept_code']        		
    			branch_code=request.POST['branch_code']
    			section=request.POST['section']
    			subsection_code=request.POST['subsection_code']

    			if 'myselection' in request.POST:
    				myselection=request.POST['myselection']
    			else:
    				myselection=0

        		Address=tblbranch.objects.get(branch_code = branch_code)


        		department = tblplatformsubjectdept.objects.get(dept_code=dept_code)

        		sec = tblplatformsections.objects.get(section=section)
        		plsub = tblplatformsubsections.objects.get(subsection_code=subsection_code)

        		bss= tblbusinesssections.objects.get(branch=Address,section=sec)

        		bsubsec = tblbusinesssubsections.objects.get(branch=Address,section=bss,subsection=plsub)

        		f= tblbusinesssubjectdept.objects.filter(branch=Address,section=bss,department=department)



        		if myselection == 'on':
        			if f.count() == 0:
        				tblbusinesssubjectdept(branch=Address,systemadmin=platformadmin, section=bss,department=department,subsection=bsubsec,status=1).save()
        				return render_to_response('platformadministrators/successfull.html')
        		else:
        			if f.count() == 1:        				
	        			f=f.get()
	        			f.delete()
	        			return render_to_response('platformadministrators/successfull.html')        	

        	else:
        		form = streamform()    		

		        return render_to_response('platformadministrators/department.html',
		            {'heading':heading,
		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def departmentview(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:

				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code,subsection,subsection_code= client.split(':')



					if  name == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Section not Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  subsection == '-----':
						msg = 'Subsection not Found'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})




					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)

						psec= tblplatformsections.objects.get(section=section)
						plsub = tblplatformsubsections.objects.get(subsection_code=subsection_code)						
						

						bsec = tblbusinesssections.objects.get(branch=Address,section=psec)
						bss = tblbusinesssubsections.objects.get(branch=Address,section=bsec, subsection=plsub)
						
						
						platformsubjectdept = tblplatformsubjectdept.objects.filter(section=psec,status=1,subsection=plsub)


						d=[]
						for k in platformsubjectdept :
							vv = tblbusinesssubjectdept.objects.filter(branch=Address,
								section= bsec,
								subsection=bss, 
								department =k, 
								status= 1)



							if vv.count() == 0:
								bb={'stream':k.dept,'alias':'Click to activate','code':k.dept_code}
							elif vv.count() ==1:
								vb=vv.get()
								bb ={'stream':k.dept,'alias':'Activated','code':k.dept_code}
							d.append(bb)



						return render_to_response('platformadministrators/department1.html',{'branch_code':branch_code,	
									'business_streams':d,'section_code':section_code,
									'bsubsection':subsection_code})

					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')

			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')




def popdepartment(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
					varuser = request.session['userid']
					user = ratifyuser(varuser)  #ON BEHALF OF

					if user['pincode'].platformadmin == True:
						post = request.POST.copy()
						code = post['userid']
						dept_code,branch_code,subsection_code, section_code = code.split(':')

						branch=tblbranch.objects.get(branch_code=branch_code)
						psec=tblplatformsections.objects.get(section_code=section_code)
						pdept = tblplatformsubjectdept.objects.get(dept_code=dept_code)						
						psub = tblplatformsubsections.objects.get(subsection_code=subsection_code)

						bsec = tblbusinesssections.objects.get(branch=branch,section=psec)
						bsub = tblbusinesssubsections.objects.get(branch=branch,section=bsec, subsection=psub)
						st = tblbusinesssubjectdept.objects.filter(department=pdept,subsection=bsub,section=bsec)

						if st.count()==0:
							du='unchecked'
							state = 'Activate'
						else:
							du='checked'
							state = 'Deactivate'


						return render_to_response('platformadministrators/department2.html',{'branch_code':branch_code,
							'school':branch,
							'sec':du,
							'subsection_code':subsection_code,
							'dept_code':dept_code,
							'dept':bsub.subsection.subsection,
							'department':pdept.dept,
							'section':psec.section,
							'state': state})



						ff=[]
						if st.count() ==1 : 
							dd = st.get()
							alias=dd.department.det
						else :
							alias =1
						s={'department':pstream.dept, 'alias':alias, 'company':branch}
						ff.append(s)
						return render_to_response('platformadministrators/department2.html',{'getdetails':ff,

							'dept_code':dept_code, 
							'section_code':section_code,
							'subsection_code':subsection_code,
							'branch_code':branch_code})





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

        if user['pincode'].platformadmin == True:

	        heading='Enter Affective'

	        platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        	if request.method=='POST':
				section_code=request.POST['section_code']        		
				branch_code=request.POST['branch_code']
				affective=request.POST['affective']

				affective_code= generate_code()


				branch =tblbranch.objects.get(branch_code = branch_code)


				psec= tblplatformsections.objects.get(section_code=section_code)

				bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

				psec = tblplatformsections.objects.get(section_code=section_code)

				bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




				f =tblbusinessaffective(platformowner= platformadmin,
					branch=branch,
					section=bsec,
					affective = affective,
					affective_code = affective_code,
					status = 1 ).save()


				return render_to_response('platformadministrators/successfull.html')         	

        	else:
				form = subsectionform()    		

				return render_to_response('platformadministrators/affective.html',
				    {'heading':heading,
				   
				    'form':form,
				    'varuser':user['varuser'],
				    'company':user['company'],
				    'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')



def viewaffec(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Select a section from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()

						if school.business_type.id ==1:

							Address=tblbranch.objects.get(branch_code = branch_code)


							psec= tblplatformsections.objects.get(section=section)

							bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

							psec = tblplatformsections.objects.get(section_code=section_code)

							bsec=tblbusinesssections.objects.get(branch=Address,section=psec)

							
							sec = tblbusinessaffective.objects.filter(	platformowner=platformadmin,
										branch=Address,
										section=bsec,
										status = 1 )


							schoolname=school.name
							addresssss=Address.address


							return render_to_response('platformadministrators/affective1.html',{'branch_code':branch_code,
							    'section_code':section_code,
							    'school':schoolname,
							    'sec':sec,
							    'address':addresssss})
						else:
							return render_to_response('platformadministrators/termname3.html')
					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')


			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')





def popviewaffec(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)


			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				section_code,branch_code=bbb.split(":")

				
				if request.method == 'POST': 

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					Address=tblbranch.objects.get(branch_code = branch_code)


					psec = tblplatformsections.objects.get(section_code=section_code)
					section = psec.section

					
					return render_to_response('platformadministrators/affective2.html',{'branch_code':branch_code,
						'k':Address,
						'section_code':section_code,
						'section':section})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






def psychomotive(request):
    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if user['pincode'].platformadmin == True:

	        heading='Enter Psychomotive'

	        platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])


        	if request.method=='POST':
				section_code=request.POST['section_code']        		
				branch_code=request.POST['branch_code']
				psychomotive=request.POST['psychomotive']

				affective_code= generate_code()


				branch =tblbranch.objects.get(branch_code = branch_code)


				psec= tblplatformsections.objects.get(section_code=section_code)

				bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

				psec = tblplatformsections.objects.get(section_code=section_code)

				bsec=tblbusinesssections.objects.get(branch=branch,section=psec)




				f =tblbusinesspsychomotive(platformowner= platformadmin,
					branch=branch,
					section=bsec,
					psychomotive = psychomotive,
					affective_code = affective_code,
					status = 1 ).save()


				return render_to_response('platformadministrators/successfull.html')         	

        	else:
				form = subsectionform()    		

				return render_to_response('platformadministrators/psycho.html',
				    {'heading':heading,
				   
				    'form':form,
				    'varuser':user['varuser'],
				    'company':user['company'],
				    'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      
    else:
        return HttpResponseRedirect('/login/')



def viewpsycho(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if user['pincode'].platformadmin == True:


				if request.method == 'POST':
					post = request.POST.copy()
					client = post['userid']

					name,school_code, address,branch_code,section,section_code= client.split(':')


					if  name == '-----':
						msg = 'Select a school from the clients list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  address == '-----':
						msg = 'Select a location from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					elif  section == '-----':
						msg = 'Select a section from the list'
						return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()

						if school.business_type.id ==1:

							Address=tblbranch.objects.get(branch_code = branch_code)


							psec= tblplatformsections.objects.get(section=section)

							bbb =tblplatformsubsections.objects.filter(	section=psec,status= 1 )

							psec = tblplatformsections.objects.get(section_code=section_code)

							bsec=tblbusinesssections.objects.get(branch=Address,section=psec)

							
							sec = tblbusinesspsychomotive.objects.filter(platformowner=platformadmin,
										branch=Address,
										section=bsec,
										status = 1 )


							schoolname=school.name
							addresssss=Address.address


							return render_to_response('platformadministrators/psycho1.html',{'branch_code':branch_code,
							    'section_code':section_code,
							    'school':schoolname,
							    'sec':sec,
							    'address':addresssss})

						else:
							return render_to_response('platformadministrators/termname3.html')
					else:
						return HttpResponseRedirect('/login/')

				else:
					return HttpResponseRedirect('/login/')


			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')





def popviewpsyche(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)


			if user['pincode'].platformadmin == True:			
				post = request.POST.copy()
				bbb = post['userid']

				section_code,branch_code=bbb.split(":")

				
				if request.method == 'POST': 

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					Address=tblbranch.objects.get(branch_code = branch_code)


					psec = tblplatformsections.objects.get(section_code=section_code)
					section = psec.section

					
					return render_to_response('platformadministrators/psycho2.html',{'branch_code':branch_code,
						'k':Address,
						'section_code':section_code,
						'section':section})


				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')





def assessement(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        valid = tbluserprofile.objects.get(email=user['varuser'])

        heading='Enter Stream'

        if valid.platformadmin == True:
        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':

        		primary=request.POST['primary']

        		if 'section' in request.POST:
        			section=request.POST['section']
        		else:
        			section  = 0

        		if section == 'on' :
        			branch_code=request.POST['branch_code']

	        		Address=tblbranch.objects.get(branch_code = branch_code)

	        		ts = tblplatformsections.objects.get(section=act)
	        		f= tblbusinesssections.objects.filter(branch=Address,section=ts)

	        		if f.count() == 0 : 
	        			tblbusinesssections(branch=Address,section=ts,status=1).save()

	        		return render_to_response('platformadministrators/successfull.html')        	


	        	else:
	        		return HttpResponseRedirect('/admin/onboarding/client/classrooms/')

        	else:
        		form = subsectionform()    		

		        return render_to_response('platformadministrators/stream.html',
		            {'heading':heading,
		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')






def assessm_ajax(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				name,school_code, address,branch_code,section,section_code= client.split(':')


				if  name == '-----':
					msg = 'Select a school from the clients list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  address == '-----':
					msg = 'Select a location from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  section == '-----':
					msg = 'Select a section from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				else:
					valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						psec= tblplatformsections.objects.get(section=section)		
						platformstream = tblplatformstreams.objects.filter(section=psec,status=1)

						bsec = tblbusinesssections.objects.get(branch=Address,section=psec)
						business_streams = tblbusinessstream.objects.filter(branch=Address,section=bsec)
						

						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/stream1.html',{'branch_code':branch_code,
							'school':schoolname,
							'business_streams':business_streams,
							'platformstream':platformstream,
							'bssection':section,
							'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






def mapping(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        valid = tbluserprofile.objects.get(email=user['varuser'])

        heading='Enter Stream'

        if valid.platformadmin == True:
        	platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

        	if request.method=='POST':

        		primary=request.POST['primary']

        		if 'section' in request.POST:
        			section=request.POST['section']
        		else:
        			section  = 0

        		if section == 'on' :
        			branch_code=request.POST['branch_code']

	        		Address=tblbranch.objects.get(branch_code = branch_code)

	        		ts = tblplatformsections.objects.get(section=act)
	        		f= tblbusinesssections.objects.filter(branch=Address,section=ts)

	        		if f.count() == 0 : 
	        			tblbusinesssections(branch=Address,section=ts,status=1).save()

	        		return render_to_response('platformadministrators/successfull.html')        	


	        	else:
	        		return HttpResponseRedirect('/admin/onboarding/client/classrooms/')

        	else:
        		form = subsectionform()    		

		        return render_to_response('platformadministrators/stream.html',
		            {'heading':heading,
		           
		            'form':form,
		            'varuser':user['varuser'],
		            'company':user['company'],
		            'pincode':user['pincode']})

        else:

        	return HttpResponseRedirect('/login/')
      

    else:
        return HttpResponseRedirect('/login/')


def mapping_ajax(request):
	if request.is_ajax():
		if  "userid" in request.session:
			varuser = request.session['userid']

			user = ratifyuser(varuser)

			if request.method == 'POST':
				post = request.POST.copy()
				client = post['userid']

				name,school_code, address,branch_code,section,section_code= client.split(':')


				if  name == '-----':
					msg = 'Select a school from the clients list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  address == '-----':
					msg = 'Select a location from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				elif  section == '-----':
					msg = 'Select a section from the list'
					return render_to_response('platformadministrators/selectloan.html',{'msg':msg})


				else:
					valid = tbluserprofile.objects.get(email=user['varuser'])

				if valid.platformadmin == True:

					platformadmin=tblplatformadministrators.objects.get(email=user['varuser'])

					school = tblschool.objects.filter(school_code=school_code,platformadmin=platformadmin)
					dt=[]


					if school.count() ==1  :
						school=school.get()
						Address=tblbranch.objects.get(branch_code = branch_code)


						psec= tblplatformsections.objects.get(section=section)		
						platformstream = tblplatformstreams.objects.filter(section=psec,status=1)

						bsec = tblbusinesssections.objects.get(branch=Address,section=psec)
						business_streams = tblbusinessstream.objects.filter(branch=Address,section=bsec)
						

						schoolname=school.name
						addresssss=Address.address


						return render_to_response('platformadministrators/stream1.html',{'branch_code':branch_code,
							'school':schoolname,
							'business_streams':business_streams,
							'platformstream':platformstream,
							'bssection':section,
							'address':addresssss})

					else:
						return HttpResponseRedirect('/login/')
				else:
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')


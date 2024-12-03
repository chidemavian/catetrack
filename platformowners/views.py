from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse


from platformowners.utils import *
from sysadmin.models import *


def welcome(request):

    if  "userid" in request.session:
        varuser = request.session['userid']

        user = ratifyuser(varuser)

        if request.method == 'POST':

        	surname = request.POST['surname']
        	firstname = request.POST['firstname']
        	othername=request.POST['othername']
        	email = request.POST['email']
        	phone = request.POST['phone']
        	staff_code = generate_code()

        	password=3

        	if 'photo' in request.FILES:
        		photo=request.FILES['photo']
        	else:
        		photo="ax/d"

        	tblstaff(branch =user['branch'],surname=surname,firstname=firstname,othername=othername,status=1,
        		email=email,staff_code=staff_code,phone=phone,photo=photo)#.save()

        	staffrec= tblstaff.objects.get(email='me@gmail.com')

        	platformowner=tblplatformowners.objects.get(email='me@gmail.com')


        	tbluserprofile(branch=user['branch'], platformadmin=1,email=email,
        		password=password,staffrec=staffrec,status=1)#.save()

        	tblplatformadministrators(platformowner=platformowner,email=email,platformadministrators_code=staff_code,status=1)#.save()

	        return render_to_response('platformowners/all_app_success.html',
	            {'varuser':user['varuser'],
	            'company':user['company'],
	            'pincode':user['pincode']})


        else:
	        return render_to_response('platformowners/createwallet.html',
	            {'varuser':user['varuser'],
	            'company':user['company'],
	            'pincode':user['pincode']})
	   

      

    else:
        return HttpResponseRedirect('/login/')
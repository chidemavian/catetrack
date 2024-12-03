from sysadmin.models import *

from business.models import *
import random




def ratifyuser(varuser):

    staff = tbluserprofile.objects.get(email=varuser,status=1)
    staffdet=staff.staffrec.id

    branch=staff.branch.id
    mycompany=staff.branch.company
    company=mycompany.name
    comp_code=mycompany.id
    ourcompay=tblschool.objects.get(id=comp_code)


    mybranch=tblbranch.objects.get(company=ourcompay,id=branch)
    admin = tblsectionmanager.objects.filter(branch=mybranch,status=1,staff=staffdet)
    staffdet = tblstaff.objects.get(email=varuser)

    user_details={'varuser':varuser,
    'company':mybranch,
    'pincode':staff,
    'admin':admin,
    'staff':staffdet,
    'branch':mybranch}

    return user_details



def generate_code():
    krt = random.randint(1,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)
    ywq = random.randint(0,9)
    xfg = random.randint(0,9)

    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) 
    return pin

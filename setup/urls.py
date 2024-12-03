from django.conf.urls import patterns, url
from django.views.generic import TemplateView
#from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = patterns('setup.views',
    # Examples:

    url(r'^welcome/$','welcome'),
    url(r'^class/$','classarm'),

    url(r'^configuration/getlocation/$','getlocation'),
    url(r'^configuration/getsection/$','getsection'),
    url(r'^configuration/getsubsection/$','getsubsection'),
    url(r'^configuration/getstream/$','getstream'),
    url(r'^configuration/getstreamajax/$','getstreamajax'),
    url(r'^configuration/popupstreamajax/$','popstreamajax'),




    url(r'^subject/$', 'subject'),
    url(r'^configuration/getdepartment/$','getdepartment'),
    url(r'^configuration/getdepartmentajax/$','getdeptajax'),



    url(r'^affective/$', 'affective'),
    url(r'^configuration/getaffectionajax/$','viewaffecajax'),



    url(r'^psychomotive/$', 'psychomotoor'),
    url(r'^configuration/getpsychoajax/$','viewpsychoajax'),



    url(r'^assessment/$', 'assessment'),
    url(r'^configuration/getpassessment/$','viewgetassessmentajax'),



    url(r'^grading/$', 'gradings'),
    url(r'^configuration/getgradingajax/$','getgradeajax'),






    # departments & roles
    url(r'^departmentsandroles/$','department'),
    # houses
    url(r'^schoolhouse/$','house'),
    url(r'^arm/$','addarm'),
    url(r'^classroom/$','myclassroom'),
    url(r'^class/delete/(\d+)/$', 'deleteclasscode'),
    url(r'^arm/delete/(\d+)/$', 'deletearmcode'),
    url(r'^getsubject/$', 'getsubject'),
    url(r'^subject_group/$','subjectgroup'),
    url(r'^subjectgroup/delete/(\d+)/$', 'deletesubjectgroupcode'),
    url(r'^editsubject/(\d+)/$', 'editsubject'),
    url(r'^house/delete/(\d+)/$', 'deletehousecode'),
    url(r'^lga/$','uploadlocalgovt'),

)


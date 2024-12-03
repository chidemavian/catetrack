from django.conf.urls import patterns, include, url


urlpatterns = patterns('platformadministrators.views',
	 url(r'^onboarding/client/$', 'homewelcome'),

	 url(r'^onboarding/client/school/$', 'newschool'),
	 url(r'^onboarding/client/school/edit/$', 'editschool'),

	 

	 url(r'^onboarding/client/branches/$', 'newbranch'),
	 url(r'^onboarding/client/branches/select/$', 'selectbranch'),



	 url(r'^onboarding/client/section/getclient/$', 'getclient'),
	 url(r'^onboarding/client/section/getlocation/$', 'getlocation'),


	 url(r'^onboarding/client/sections/$', 'newsection'),
	 url(r'^onboarding/client/section/select/view/$', 'selectsection'),

	 url(r'^onboarding/client/sections/enter/$', 'entersection'),


	 url(r'^onboarding/client/section/getsubsections/$', 'getsubsection'),

	url(r'^onboarding/client/subsection/getsubsection/$', 'getsubsection'),

	 url(r'^onboarding/client/subsections/$', 'subsection'),
	 url(r'^onboarding/client/section/getsections/$', 'getsection'),
	 url(r'^onboarding/client/view/subsection/$', 'subsectview'),
	 url(r'^onboarding/client/select/subsection/$', 'subsec'),	



	 url(r'^onboarding/client/apps/$', 'setapp'),
	 url(r'^onboarding/client/apps/select/view/$', 'selectapp'),
	 url(r'^onboarding/client/select/popapp/$', 'sectionapp'),


	 url(r'^onboarding/client/termnames/$', 'termnames'),
	 url(r'^onboarding/client/termnames/select/$', 'settermname'),
	 url(r'^onboarding/client/term/termpop/$', 'termpop'),




	 url(r'^onboarding/client/classrooms/$', 'streamm'),
	 url(r'^onboarding/client/streamview/$', 'streamviw'),

	 url(r'^onboarding/client/classrooms/popstream/$', 'popstreamm'),





	 url(r'^onboarding/client/departments/$', 'department'),
	 url(r'^onboarding/client/departmentview/$', 'departmentview'),

	 url(r'^onboarding/client/dept/popdepartment/$', 'popdepartment'),



	 url(r'^onboarding/client/affective/$', 'affective'),
	 url(r'^onboarding/client/view/affective/$', 'viewaffec'),

	 url(r'^onboarding/client/popview/affective/$', 'popviewaffec'),




	 url(r'^onboarding/client/psycho/$', 'psychomotive'),
	 url(r'^onboarding/client/view/psycho/$', 'viewpsycho'),

	 url(r'^onboarding/client/popview/psycho/$', 'popviewpsyche'),




	 url(r'^onboarding/client/subjects/$', 'subjects'),
	 url(r'^onboarding/client/subjects/select/view/$', 'selectsubject'),



	 url(r'^onboarding/client/reportsheet/$', 'reportsheet'),
	 url(r'^onboarding/client/assessmet/reportajax/$', 'reportsheetajax'),



	 url(r'^onboarding/client/assessments/$', 'assessment'),
	 url(r'^onboarding/client/assessmet/asesajax/$', 'assessementajax'),


	 url(r'^onboarding/client/mapping/$', 'mapping'),
	 url(r'^onboarding/client/mapping/maajax/$', 'mapping_ajax'),



	 url(r'^onboarding/client/schooladmin/$', 'newadmin'),
	 url(r'^onboarding/client/schooladmin/select/view/$', 'setadmin'),
 



	 )
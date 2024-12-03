
from django.conf.urls import patterns, url
from django.views.generic import DetailView, TemplateView
urlpatterns = patterns('CBT.views',
    
    url(r'^home/$', 'chroose'),
    url(r'^set_user/subject/$', 'assignment'),
 

    ###****questions************
    url(r'^enter/question/$', 'qstn'),
    url(r'^enter/image/(\d+)/$', 'cbtimage'),
    url(r'^enter/ajaxclass/$', 'ajaxclass'),
    url(r'^getcbtsubject/$', 'getcbtsubject'),

    url(r'^enter/question/getqstn/$', 'getcbtqst'),
    
    url(r'^enter/question/ajax/$', 'editcbtqst'),

    url(r'^enter/question/majax/$', 'editcbtpix'),




###English************
url(r'^enter/question/english/$', 'english'),#

url(r'^enter/question/comprehension/$', 'comprqstn'), #compreh quest instr redirect


url(r'^enter/question/bblock/$', 'bblock'), #block instr redirect

url(r'^enter/question/bblock/qstns/$', 'bblockqstn'), #block qstn redirect

url(r'^enter/question/others/oqstns/$', 'otherqstn'), #block qstn redirect

url(r'^enter/question/getengobjqstn/$', 'getcbtengqst'),

url(r'^enter/question/compqst/$', 'compquest'),# #compr questn



url(r'^enter/question/getengoblk/$', 'getcbtengblk'),
url(r'^enter/question/blkqst/$', 'allblkq'),#

url(r'^enter/question/editblkqst/$', 'editallblkq'),#

url(r'^enter/question/editblkqstinst/$', 'editallinstr'),#

url(r'^enter/question/chninst/(\d+)/$', 'installblkq'),#

url(r'^enter/blkquestion/editblkqst/$', 'editblktxtqst'),#
url(r'^enter/question/instchh/(\d+)/$', 'instchh'),#




url(r'^enter/option/blkedt/$', 'editqstbblk'),
url(r'^enter/optionA/changeblkA/(\d+)/$', 'editoptioblkA'),
url(r'^enter/optionA/changeblkimageA/(\d+)/$', 'editoptiobimagelkA'),





url(r'^enter/option/blkedtb/$', 'editqstbblkb'),
url(r'^enter/optionA/changeblkB/(\d+)/$', 'editoptioblkB'),
url(r'^enter/optionA/changeblkimageB/(\d+)/$', 'editoptiobimagelkB'),


url(r'^enter/option/blkedtc/$', 'editqstbblkc'),
url(r'^enter/optionA/changeblkC/(\d+)/$', 'editoptioblkC'),
url(r'^enter/optionA/changeblkimageC/(\d+)/$', 'editoptiobimagelkC'),


url(r'^enter/option/blkedtd/$', 'editqstbblkd'),
url(r'^enter/optionA/changeblkD/(\d+)/$', 'editoptioblkD'),
url(r'^enter/optionA/changeblkimageD/(\d+)/$', 'editoptiobimagelkD'),


url(r'^enter/blkoption/answers/$', 'editblkans'),
url(r'^enter/option/changeblkans/(\d+)/$', 'changeblkans'),#


url(r'^enter/option/othersedit/$', 'editqstodaspop'),
url(r'^enter/qstn/otherss/(\d+)/$', 'editqstodas'),#

url(r'^enter/option/otherseditimag/$', 'editqstodasimagepop'),
url(r'^enter/qstnimage/oda/(\d+)/$', 'editqstodasimage'),#



url(r'^enter/blkquestion/saveblkqst/(\d+)/$', 'editsaveblk'),#
url(r'^enter/blkquestion/saveblkqstimage/(\d+)/$', 'editsaveblki'),#

url(r'^enter/question/cngblkqstt/(\d+)/$', 'cngblkqstt2'),#


url(r'^enter/question/getblockqst/$', 'getblockqst'),#



url(r'^enter/question/addblkqst/$', 'addsomblkqst'),#
url(r'^enter/question/blockq/(\d+)/$', 'blkuestion'),#

url(r'^enter/question/justeditblkqst/$', 'blkqstedit'),#






url(r'^enter/question/getothers/$', 'getothers'),





url(r'^enter/option/otheredt/$', 'editoptodaspop'),
url(r'^enter/optionA/otherschangeA/(\d+)/$', 'editoptionodaA'),
url(r'^enter/changeoptionA/othersimagechangeA/(\d+)/$', 'chngoptiobimageA'),


url(r'^enter/option/otheredtB/$', 'editoptodaspopB'),
url(r'^enter/optionA/otherschangeB/(\d+)/$', 'editoptionodaB'),
url(r'^changeoptionb/othersimagechangeB/(\d+)/$', 'chngoptiobimageB'),




url(r'^enter/option/otheredtC/$', 'editoptodaspopC'),
url(r'^enter/optionA/otherschangeC/(\d+)/$', 'editoptionodaC'),
url(r'^changeoptionb/othersimagechangeC/(\d+)/$', 'chngoptiobimageC'),



url(r'^enter/option/otheredtD/$', 'editoptodaspopD'),
url(r'^enter/optionA/otherschangeD/(\d+)/$', 'editoptionodaD'),
url(r'^changeoptionb/othersimagechangeD/(\d+)/$', 'chngoptiobimageD'),


url(r'^enter/otheroption/answerss/$', 'editotherans'),
url(r'^enter/option/changeotherans/(\d+)/$', 'changeotherans'),#




url(r'^enter/question/englishajax/$', 'popeditx'),

 url(r'^enter/image/english/(\d+)/$', 'popengl'),

url(r'^enter/options/alleng/$', 'getcats'),

url(r'^editallentries/$', 'editallentry'),

url(r'^enter/options/compre/$', 'entcompopt'), #comp opti pop up

url(r'^options/enter/compre/options/(\d+)/$', 'entercompoptions'),

url(r'^enter/qst/edt/$', 'edtcompqst'),


url(r'^enter/option/edt/$', 'edtoptt'),
url(r'^enter/optionA/changeA/(\d+)/$', 'editoptioA'),


url(r'^enter/option/edtb/$', 'edtopttb'),
url(r'^enter/optionA/changeb/(\d+)/$', 'editoptioB'),

url(r'^enter/option/edtc/$', 'edtopttc'),
url(r'^enter/optionA/changec/(\d+)/$', 'editoptioC'),


url(r'^enter/option/edtd/$', 'edtopttd'),
url(r'^enter/optionA/changed/(\d+)/$', 'editoptioD'),






url(r'^enter/option/answers/$', 'edtans'),
url(r'^enter/option/changeans/(\d+)/$', 'changeansw'),#

url(r'^enter/options/blockqstin/$', 'blkoption'),
url(r'^options/engblk/texts/(\d+)/$', 'blktextts'),
url(r'^input_text/blkqst/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_blktext'),
url(r'^enter/blkoptions/(\d+)/$', 'myblkoptions'),


url(r'^enter/options/odaoption/$', 'otheroption'),
url(r'^options/engothers/odatexts/(\d+)/$', 'othertextts'),
url(r'^options/chooseothers/imagesothers/(\d+)/$', 'imagesothers'),

url(r'^otherqst/input_otherimages/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_othermages'),

url(r'^otherqst/options/eng/imageother/(\d+)/$', 'odaoptionsimage'),

url(r'^input_text/otherssqst/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_othertext'),
url(r'^enter/otheroptions/(\d+)/$', 'myotheroptions'),




url(r'^options/choose/images/(\d+)/$', 'imagesp'),

url(r'^blkqst/input_images/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_blkimages'),

url(r'^blkqst/options/eng/image/(\d+)/$', 'blkoptionsimage'),




url(r'^take_test/english/start/$', 'pushstart'),
 url(r'^take_test_eng/spin/$', 'spin'),
 url(r'^take_test_eng/wheel/$', 'wheel'),

 url(r'^take_test_eng/nextng/$', 'engnext'),

 url(r'^take_test_engprev/nexprev/$', 'prenext'),



##*******options *******************
    url(r'^options/$', 'options'),
    url(r'^enter/options/getopt/$', 'getcbtopt'),
    url(r'^enter/englishh/options/getopt/$', 'getcbtengedit'),
    url(r'^options/options/(\d+)/$', 'myoptions'),
    url(r'^options/options/image/(\d+)/$', 'myoptionsimage'),
    url(r'^options/enteropt/$', 'optajax'),

    url(r'^options/choose/$', 'chooseopt'),

    url(r'^options/enlarge/$', 'enlarge'),
    url(r'^options/texts/(\d+)/$', 'textts'),
    url(r'^input_text/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_text'),
    url(r'^options/images/(\d+)/$', 'images'),
    url(r'^input_images/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'save_images'),



# #***--------------theory------------------
    url(r'^enter/theory/$', 'theory'),
    url(r'^getmytheoryquestons/$', 'gettheoryajax'),
    url(r'^deletheoajax/$', 'deltheory'),
    url(r'^enter/theory/yesdel/(\d+)/$', 'theorydelete'),

    ##****** student's view exams**************
    url(r'^cbt/exam/$', 'exxxam'),
    url(r'^take_test/start/$', 'pupilcbt'),
    url(r'^take_test/next/$', 'next'),
    url(r'^take_test/submit/$', 'submitnext'),
   
    url(r'^take_test/previous/$', 'beefore'),
    url(r'^take_test/skip/$', 'skip'),
  url(r'^pupil/scripts/$', 'my_scripts'),
  url(r'^take_test/previous/done/$', 'donebee'),
    url(r'^take_test/mytheory/$','qtheory'),

    ##*******edit *******************
    url(r'^enter/options/edit/$', 'editquestion'),
    url(r'^edit/$', 'editq'),
  
    url(r'^edit/editentry/$', 'doentry'),


    url(r'^edit/editqst/$', 'editqst'),
    url(r'^change/question/(\d+)/$', 'changeqst'),


    url(r'^edit/edita/$', 'editoptiona'),
    url(r'^change/optiona/(\d+)/$', 'optiona'),

    url(r'^edit/editb/$', 'editoptionb'),
    url(r'^change/optionb/(\d+)/$', 'optionb'),

    url(r'^edit/editc/$', 'editoptionc'),
    url(r'^change/optionc/(\d+)/$', 'optionc'),

    url(r'^edit/editd/$', 'editoptiond'),
    url(r'^change/optiond/(\d+)/$', 'optiond'),

    url(r'^edit/imageqst/$', 'sdfgsf'),


    url(r'^question/imageedit/(\d+)/$', 'chngqstimage'),

#**********##mark guides*********************
    url(r'^mark_guides/$', 'markguide'),

    url(r'^markguide/getmg/$', 'guides'),    

    url(r'^assessment/set/$', 'setass'),  

    #***************schedulling####
    url(r'^assess/getassess/$', 'getassessment'),
   url(r'^schedulling/active/$', 'cbtstat'),
    url(r'^getsubject/$', 'getcbtsub'),
    url(r'^getterm/$', 'getterm'),

    url(r'^delete/schedule/ajax/$', 'deletesch'),

    url(r'^delete/sche/no/$', 'noscheajax'),

    url(r'^delete/sche/yes/(\d+)/$', 'yessche'),

    url(r'^getscheduledsubject/$', 'getscheduledsubject'), 
    url(r'^getcbtklass/$', 'getcbtklass'), 
    url(r'^access_denied/$', 'unautho'), 


###***User***********
url(r'^finduser/$', 'autocomplete'),
url(r'^delete/user/ajax/$', 'userdelete'), 
url(r'^delete/user/no/$', 'noajax'),
url(r'^delete/user/yes/(\d+)/$', 'yesajax'),

###***Print***********
url(r'^print/$', 'printper'),
url(r'^getstudent/$', 'getstudent'),

###***exam officer***********
url(r'^getallusers/$', 'userlist'),
##***********Exam type*************
url(r'^getexam/$', 'getactiveexam'),


###Miscellenous***********
url(r'^miscellenous/student', 'miscellenous'),



#previous for english
url(r'^take_test/enggglish/previous/$', 'nabefore'),


#next for english
url(r'^take_test/enggglish/push/$', 'nabpush'),

url(r'^take_test_eng/rnewwheel/$', 'renew'),
    )

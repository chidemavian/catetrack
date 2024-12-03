



from django.shortcuts import render_to_response


from django.core.mail import send_mail


from CBT.models import *




import random



from datetime import *


dddy = datetime.today()
ttimee = dddy.time()



def mytime(student,duration,start_time,extention):
    elapsed_time = ttimee - start_time
    t = duration + extention - elapsed_time
    return t



def generate_blk_pin():
    krt = random.randint(1,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)
    ywq = random.randint(0,9)
    xfg = random.randint(0,9)
    zvv = random.randint(0,9)
    a = random.randint(0,9)
    hzp = random.randint(0,9)
    yq = random.randint(0,9)
    xj = random.randint(0,9)
    zp = random.randint(0,9)
    au = random.randint(0,9)
    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) + str(zvv)+ str(a) + str(hzp) + str(yq) + str(xj) + str(zp)+ str(au)

    return pin







def display_answered_qstn(code,category,number):
    if category == 'C':
        myq=tblcomprehensionqst.objects.get(qstcode=code)
        image = 'myq.image'
        pos = 'pos'


        opt = tbloptionseng.objects.get(qstn = myq)
    

        qq=  number


    elif category == 'block':
        myq=tblblockquestion.objects.get(qstcode=code)
        image = myq.image

        try :
            opt = tbloptionblk.objects.get(qstn=myq)
            pos = 'low'
        except:
            opt = tbloptionblki.objects.get(qstn = myq)
            pos = 'hi'

        qq=  number
        

    elif category == 'others':
        myq=tblothers.objects.get(qstcode=code)

        image = myq.image

        try :
            opt = tbloptionsothers.objects.get(qstn=myq)
            pos = 'low'
        except:
            opt = tbloptionothersi.objects.get(qstn = myq)
            pos = 'hi'
        qq=  number

    return {'qq':qq,'image':image,'options':opt,'question':myq,'pos':pos}
    


def questioncount(session,klass,term,subject,exam_type):

# 1 comprehension questions
    comp = tblcomprehension.objects.filter(
        session=session,
        klass=klass,
        subject=subject,
        term = term,
        exam_type=exam_type)

    d1 = tblcomprehensionqst.objects.filter(comprehension=comp)
    d1 = d1.count()
    
    blk= tblblock.objects.filter(session=session,
        term = term,
        exam_type=exam_type)

    
# 2 block questions

    gg =0
    for hj in blk:
        d2 = tblblockquestion.objects.filter(block=hj).count()
        gg=gg+d2


    mbg=d1 + gg



# 3 other questions

    oda = tblothers.objects.filter(
        session=session,
        klass=klass,
        subject=subject,
        term = term,
        exam_type=exam_type)

    d14 = oda.count()


    mbg=mbg +  d14





    return mbg






def total_ans_qst(session,term,subject,student,exam_type):


 #total number of answered question

    done_blk_qst = tblcbttranscomp.objects.filter(session=session,
        term=term,subject=subject,exam_type=exam_type,student=student) 

    tcount= done_blk_qst.count()

    return tcount




def current_question(session,term,subject,student,exam_type):

    #import details of the current question   


    disp_no = tblcbtcurrentquestioneng.objects.filter(session=session,term=term,
        subject=subject,student=student, exam_type=exam_type)

    if disp_no.count() == 1:
        disp_no = disp_no.get()

        disp_no_number = disp_no.number

        actual_qst = tblcbtoldeng.objects.get(question=disp_no,qstno=disp_no_number)
        
        category  = actual_qst.category

        qstn_code = actual_qst.qstcode

        number=actual_qst.qstno
        groupcode= actual_qst.groupcode

        d= {'groupcode':groupcode,'code':qstn_code, 'category':category,'number':number,
        'asd':disp_no,'q_code':actual_qst}

    else:

        d= {'code':0,'category':0,'number':0,'groupcode':0}

    return d





def transition_to_another_blk(session,term,subject,student,exam_type,category):


    ###step 1, choose a block random question

    if category == 'block':
        blok  =  tblblock.objects.filter(session=session,term=term,exam_type=exam_type,
            subject=subject)

        ramk = [ str(k.code) for k in blok ]
        ram=0
        chh=0

        hhh =[]

        for h in ramk:
            bloky = blok.get(code = h)

            #how many questions has this block
            blk_qst = tblblockquestion.objects.filter(block = bloky)


            #how many questions from this block have you answered
            total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = h,
                term=term,subject=subject,exam_type=exam_type,student=student)


            ansd_id = [str(k.qstcode) for k in total_ansd]

            #how many questions from this block are unanswered
            hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

            hgy_count = len(hgy)

            if hgy_count != 0:
                for j in hgy :
                    hhh.append(j)

         
        if len(hhh)>0 :

            chh =random.choice(hhh)

    ###step 2, question details

            blk4 = tblblockquestion.objects.get(qstcode = chh)
            groupcode = blk4.block.code
            groupcode= tblblock.objects.get(code=groupcode)


            #how many questions has this block
            blk_qst = tblblockquestion.objects.filter(block = groupcode)



            #how many questions from this block have you answered
            total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode,
                term=term,subject=subject,exam_type=exam_type,student=student)



            ansd_id = [str(k.qstcode) for k in total_ansd]

            #how many questions from this block are unanswered
            hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

            hgy_count = len(hgy)


            tty ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':hgy_count,'question':blk4}

        
        else:
            tty ={'total':0, 'solved':0,'remain':0,'question':0}


    return tty




def transition_to_others(session,term,subject,student,exam_type,category):

    if category == 'others':

        #how many questions has this block
        odas  =  tblothers.objects.filter(session=session,term=term,exam_type=exam_type,
            subject=subject)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,category = 'others',
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in odas if str(k.qstcode) not in ansd_id]

        hgy_count=len(hgy)

         
        if len(hgy)>0 :

            chh =random.choice(hgy)

            blk4  =  tblothers.objects.get(session=session,term=term,exam_type=exam_type,
                qstcode=chh,subject=subject)

            tty ={'total':odas.count(), 'solved':total_ansd.count(),'remain':hgy_count,'question':blk4}

        
        else:
            tty ={'total':0, 'solved':0,'remain':0,'question':0}


    return tty




def blk_count(session,term,subject,exam_type,category,groupcode):


    ###step 1, total block question

    if category == 'block':
        blok  =  tblblock.objects.filter(session=session,term=term,exam_type=exam_type,
            subject=subject,code=groupcode)

        ramk = len(blok)


    return ramk



def Next_unanswered_blk_question(session,term,subject,student,exam_type,category,groupcode,klass):


    ###step 1, choose a block random question

    if category == 'block':
        bloky  =  tblblock.objects.get(session=session,term=term,
            exam_type=exam_type,
            subject=subject,code=groupcode,
            klass=klass)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

    return hgy





def retrieve_question_detailblk(code,student):

    ram = tblblockquestion.objects.get(qstcode=code)
    gp = ram.block.code

    blk = tblblock.objects.get(code = gp)


    #how many questions has this block
    gp_count = tblblockquestion.objects.filter(block=blk)


    #how many questions from this block have you answered
    total_ansd = tblcbttranscomp.objects.filter(groupcode = gp,student=student)
    ansd_id = [str(k.qstcode) for k in total_ansd]


    #how many questions from this block are unanswered
    bk= [ str(k.qstcode) for k in gp_count if str(k.qstcode) not in ansd_id]


    pt ={'total':gp_count.count(), 'solved':total_ansd.count(),'remain':len(bk),'question':ram}

    return pt




def Next_unanswered_blk_question_spin(session,term,subject,student,exam_type,category,groupcode,klass,code):


    ###step 1, choose a block random question

    if category == 'block':
        bloky  =  tblblock.objects.get(session=session,term=term,
            exam_type=exam_type,
            subject=subject,code=groupcode,
            klass=klass)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

        if len(hgy) >1:

            return [ k for k in hgy if k not in code]

        else:
            return hgy




def retrieve_comprehension_question_detail(code,student):

    ram = tblcomprehensionqst.objects.get(qstcode=code)
    comprehension = ram.comprehension.id


    #how many questions has this passage
    gp_count = tblcomprehensionqst.objects.filter(comprehension = comprehension)


    #how many questions from this passage have you answered
    total_ansd = tblcbttranscomp.objects.filter(groupcode = 'fu',student=student)
    ansd_id = [str(k.qstcode) for k in total_ansd]


    #how many questions from this passage are unanswered
    bk= [ str(k.qstcode) for k in gp_count if str(k.qstcode) not in ansd_id]


    pt ={'total':gp_count.count(), 'solved':total_ansd.count(),'remain':len(bk),'question':ram}

    return pt

































def transition_blk_others(session,term,subject,student,exam_type,klass):



    blok  =  tblblock.objects.filter(session=session,term=term,exam_type=exam_type,
        subject=subject)

    ramk = [ str(k.code) for k in blok ]
    ram=0
    chh=0

    hhh =[]

    for h in ramk:
        bloky = blok.get(code = h)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = h,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

        hgy_count = len(hgy)

        if hgy_count != 0:
            for j in hgy :
                kl = {'code':j,'groupcode':h}
                hhh.append(kl)



    qst = tblothers.objects.filter(session=session,
        term= term,klass=klass,
        subject=subject,exam_type=exam_type)

    total_ansd_ot = tblcbttranscomp.objects.filter(session=session,
        term=term,subject=subject,
        exam_type=exam_type,
        groupcode='AA',student=student)

    ansdid= [k.qstcode for k in total_ansd_ot]

    ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]

    ram_count = len(ram)


    if ram_count != 0:
        for jh in ram :
            kl = {'code':jh,'groupcode':"AA"}
            hhh.append(kl)


    if len(hhh)>0 :

        chh =random.choice(hhh)


        if chh['groupcode'] != 'AA':

                ###step 2, question details

            blk4 = tblblockquestion.objects.get(qstcode = chh['code'])
            groupcode1 = blk4.block.code
            groupcode= tblblock.objects.get(code=groupcode1)


            #how many questions has this block
            blk_qst = tblblockquestion.objects.filter(block = groupcode)



            #how many questions from this block have you answered
            total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode1,
                term=term,subject=subject,exam_type=exam_type,student=student)



            ansd_id = [str(k.qstcode) for k in total_ansd]

            #how many questions from this block are unanswered
            hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

            hgy_count = len(hgy)


            tty ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':hgy_count,'question':blk4,'groupcode':groupcode1}

        

        else:

            blk44 = tblothers.objects.get(qstcode = chh['code'])

            tty ={'total':qst.count(), 'solved':total_ansd_ot.count(),'remain':ram_count,'question':blk44,'groupcode':'AA'}
 

    else:
        tty ={'total':0, 'solved':0,'remain':0,'question':0}


    

    return tty




def wheel_from_everywhere(session,term,subject,student,exam_type,groupcode,qstcode, klass):


 

    blok  =  tblblock.objects.filter(session=session,term=term,exam_type=exam_type,
        subject=subject)

    ramk = [ str(k.code) for k in blok ]

    if groupcode != 'AA':
        ramk = [k for k in ramk if k not in groupcode]

    ram=0
    chh=0

    hhh =[]

    for h in ramk:
        bloky = blok.get(code = h)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = h,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

        hgy_count = len(hgy)

        if hgy_count != 0:
            for j in hgy :
                kl = {'code':j,'groupcode':h}
                hhh.append(kl)



    qst = tblothers.objects.filter(session=session,
        term= term,klass=klass,
        subject=subject,exam_type=exam_type)

    total_ansd_ot = tblcbttranscomp.objects.filter(session=session,
        term=term,subject=subject,
        exam_type=exam_type,
        groupcode='AA',student=student)

    ansdid= [k.qstcode for k in total_ansd_ot]

    ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]

    ram_count = len(ram)


    if ram_count != 0:
        for jh in ram :
            kl = {'code':jh,'groupcode':"AA"}
            hhh.append(kl)


    if len(hhh)>0 :

        chh =random.choice(hhh)


        if chh['groupcode'] != 'AA':

                ###step 2, question details

            blk4 = tblblockquestion.objects.get(qstcode = chh['code'])
            groupcode1 = blk4.block.code
            groupcode= tblblock.objects.get(code=groupcode1)


            #how many questions has this block
            blk_qst = tblblockquestion.objects.filter(block = groupcode)



            #how many questions from this block have you answered
            total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode1,
                term=term,subject=subject,exam_type=exam_type,student=student)



            ansd_id = [str(k.qstcode) for k in total_ansd]

            #how many questions from this block are unanswered
            hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

            hgy_count = len(hgy)


            tty ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':hgy_count,'question':blk4,'groupcode':groupcode1}

        

        else:

            blk44 = tblothers.objects.get(qstcode = chh['code'])

            tty ={'total':qst.count(), 'solved':total_ansd_ot.count(),'remain':ram_count,'question':blk44,'groupcode':'AA'}
 

    else:
        tty ={'total':0, 'solved':0,'remain':0,'question':0}




    return tty





def Next_unanswered_compre_qst(session,term,subject,student,exam_type,category,klass):

    #question ids of unanswered comprehension questions

    if category == 'C':

        comprehension =  tblcomprehension.objects.get(session=session,
            term=term,exam_type=exam_type,
            subject=subject,klass=klass)

        qst = tblcomprehensionqst.objects.filter(comprehension = comprehension)
        b= qst.count()


        total_ansd = tblcbttranscomp.objects.filter(session=session,
            term=term,subject=subject, exam_type=exam_type,
            groupcode='fu', student=student)

        ansdid= [k.qstcode for k in total_ansd]

        ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]

        if len(ram) > 0:

            ddd= random.choice(ram)

            myram = qst.get(qstcode=ddd)
     

            pt ={'total':b, 'solved':total_ansd.count(),'remain':len(ram),'question':myram}
        else:

            pt ={'total':b, 'solved':total_ansd.count(),'remain':len(ram),'question':0}


    return pt


def spin_compre_qst(session,term,subject,student,exam_type,category,klass,qstcode):

    #question ids of unanswered comprehension questions

    if category == 'C':

        comprehension =  tblcomprehension.objects.get(session=session,
            term=term,exam_type=exam_type,
            subject=subject,klass=klass)

        qst = tblcomprehensionqst.objects.filter(comprehension = comprehension)
        b= qst.count()


        total_ansd = tblcbttranscomp.objects.filter(session=session,
            term=term,subject=subject, exam_type=exam_type,
            groupcode='fu', student=student)

        ansdid= [k.qstcode for k in total_ansd]

        ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]

        fg = ram

        if len(ram) >1:
            ram = [k for k in ram if k not in qstcode]

        ddd= random.choice(ram)

        myram = qst.get(qstcode=ddd)
 
        pt ={'total':b, 'solved':total_ansd.count(),'remain':len(fg),'question':myram}
   


    return pt

































def Next_unanswered_blk2_question(session,term,subject,student,exam_type,category,groupcode,klass):


    ###step 1, choose a block random question

    if category == 'block':
        bloky  =  tblblock.objects.get(session=session,term=term,
            exam_type=exam_type,
            subject=subject,code=groupcode,
            klass=klass)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]


        if len(hgy)>0:

            disp_qst_code = random.choice(hgy)

            ram = blk_qst.get(qstcode=disp_qst_code)

            pt ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':len(hgy),'question':ram}

        else:

            pt ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':len(hgy),'question':0}

    
    return pt



def spin_blk(session,term,subject,student,exam_type,category,groupcode,klass,qstcode):


    ###step 1, choose a block random question

    if category == 'block':
        bloky  =  tblblock.objects.get(session=session,term=term,
            exam_type=exam_type,
            subject=subject,code=groupcode,
            klass=klass)

        #how many questions has this block
        blk_qst = tblblockquestion.objects.filter(block = bloky)


        #how many questions from this block have you answered
        total_ansd = tblcbttranscomp.objects.filter(session=session,groupcode = groupcode,
            term=term,subject=subject,exam_type=exam_type,student=student)


        ansd_id = [str(k.qstcode) for k in total_ansd]

        #how many questions from this block are unanswered
        hgy= [ str(k.qstcode) for k in blk_qst if str(k.qstcode) not in ansd_id]

        g2 = hgy


        if len(hgy)>1:
            hgy= [p for p in hgy if p not in qstcode]


        disp_qst_code = random.choice(hgy)

        ram = blk_qst.get(qstcode=disp_qst_code)

        pt ={'total':blk_qst.count(), 'solved':total_ansd.count(),'remain':len(g2),'question':ram}

    
    
    return pt



















































































def Next_unanswered2_others_question(session,term,subject,student,exam_type,category,klass):

    #question ids of unanswered comprehension questions

    if category == 'others':

        qst = tblothers.objects.filter(session=session,
            term= term,klass=klass,
            subject=subject,exam_type=exam_type)

        ccount=qst.count()

        total_ansd = tblcbttranscomp.objects.filter(session=session,
            term=term,subject=subject,
            exam_type=exam_type,
            groupcode='AA',student=student)

        ansdid= [k.qstcode for k in total_ansd]

        ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]



        if len(ram) >0:
            disp_qst_code = random.choice(ram)
            nxt_q = qst.get(qstcode=disp_qst_code)
            pt ={'total':ccount, 'solved':total_ansd.count(),'remain':len(ram),'question':nxt_q}
        
        else:
            pt ={'total':ccount, 'solved':total_ansd.count(),'remain':len(ram),'question':0}

    return pt






def spin_others(session,term,subject,student,exam_type,klass,code):

    qst = tblothers.objects.filter(session=session,
        term= term,klass=klass,
        subject=subject,exam_type=exam_type)

    total_ansd_ot = tblcbttranscomp.objects.filter(session=session,
        term=term,subject=subject,
        exam_type=exam_type,
        groupcode='AA',student=student)

    ansdid= [k.qstcode for k in total_ansd_ot]

    ram = [ str(k.qstcode) for k in qst if str(k.qstcode) not in ansdid]

    gt = ram

    if len(ram)>1:
        ram = [h for h in ram if h not in code]


    chh =random.choice(ram)

    blk44 = tblothers.objects.get(qstcode = chh)

    tty ={'total':qst.count(), 'solved':total_ansd_ot.count(),'remain':len(gt),'question':blk44,'groupcode':'AA'}
 

    return tty
from academics.models import *
from student.models import *


def classavg(self):
    a = SubjectScore.objects.filter(subject=self.subject, term=self.term,
        session=self.session, klass=self.klass,
        arm=self.arm).aggregate(Avg('end_term_score'))
    kk = a['term_score__avg']
    return kk

def juniorgrade(score):
    if (score >=90) and (score <= 100):
        grade = 'A+'
        remark = 5
    elif (score >=75) and (score <= 90.9):
        grade = 'A'
        remark = 4.5
    elif (score >=65) and (score <= 74.9):
        grade = 'B'
        remark = 4
    elif (score >=50) and (score <= 64.9):
        grade = 'C'
        remark = 3
    elif (score >=45) and (score <= 49.9):
        grade = 'D'
        remark = 2
    elif (score >=40) and (score <= 44.9):
        grade = 'E'
        remark = 1
    elif (score >=1) and (score <= 39.9):
        grade = 'F'
        remark = 1
    else:
        grade = 'F'
        remark =0
    return {'remark':remark,'grade':grade}


def seniorgrade(score):
    if (score >=80) and (score <= 100):
        grade = 'A1'
        remark = 5
    elif (score >=75) and (score <= 79.99):
        grade = 'B2'
        remark = 4.5
    elif (score >=70) and (score <= 74.99):
        grade = 'B3'
        remark = 4
    elif (score >=65) and (score <= 69.99):
        grade = 'C4'
        remark = 3.5
    elif (score >=60) and (score <= 64.99):
        grade = 'C5'
        remark = 3
    elif (score >=50) and (score <= 59.99):
        grade = 'C6'
        remark = 2.5
    elif (score >=45) and (score <= 49.99):
        grade = 'D7'
        remark = 2
    elif (score >=40) and (score <= 44.99):
        grade = 'E8'
        remark = 1.5
    elif (score >=0) and (score <= 39.99):
        grade = 'F9'
        remark = 1
    else:
        grade =0
        remark = 0
    return {'remark':remark,'grade':grade}




def studentaveragedrader(score):
    if (score >=80) and (score <= 100):
        grade = 'A'
        remark = 5
    elif (score >=70) and (score <= 79.99):
        grade = 'B'
        remark = 4
    elif (score >=50) and (score <= 69.99):
        grade = 'C'
        remark = 3
    elif (score >=45) and (score <= 49.99):
        grade = 'D'
        remark = 2
    elif (score >=40) and (score <= 44.99):
        grade = 'E'
        remark = 1
    elif (score >=0) and (score <= 39.99):
        grade = 'F'
        remark = 0
    else:
        grade =0
        remark = 0
    return {'remark':remark,'grade':grade}

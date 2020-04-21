from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import List,studList,instructors,links,assignments,announcements,studRecords,questr,ques,attempt,resAccess,topic,qnr_attempt,qn_attempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Avg,Sum
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
import pandas as pd
import numpy as np
import datetime
import csv
def Link2(request):
    if request.user.is_authenticated and not request.user.profile.ifTeacher:
        all_items=List.objects.all
        return render(request, 'Link2.html', {'all_items':all_items})
    elif request.user.is_authenticated and request.user.profile.ifTeacher:
        if request.method=='POST':
            it=request.POST['item']
            if List.objects.filter(item=it).exists():
                messages.warning(request,('Course already exists!'))
            else:
                a=List(item=it)
                a.save()
            all_items=List.objects.all
            return render(request, 'Link2.html', {'all_items':all_items})
        else:
            all_items=List.objects.all
            return render(request, 'Link2.html', {'all_items':all_items})
    else:
        return redirect('login_S')

def crossofff(request,list_id):
    if not request.user.is_authenticated:
        return redirect('Link2')
    item=List.objects.get(pk=list_id)
    em=request.user.username
    try:
        s=studList.objects.get(email=em,course=item)
        s.stat=True
        s.save()
        messages.success(request,('You have registered for this course successfully!'))
    except:
        messages.warning(request,('You are not eligible to register for this course!'))
    return redirect('Link2')

def courseRO(request,cid):
    if not request.user.is_authenticated:
        return redirect('Link2')
    course=List.objects.get(pk=cid)
    i=instructors.objects.filter(course=course)
    l=links.objects.filter(course=course)
    ass=assignments.objects.filter(course=course)
    ann=announcements.objects.filter(course=course)
    topics=topic.objects.filter(course=course)
    it=studRecords(name=request.user.first_name,email=request.user.username,course=course.item,DT=datetime.datetime.now())
    it.save()
    return render(request, 'courseInfoRO.html', {'cid':cid,'course':course,'topics':topics,'i':i,'l':l,'ass':ass,'ann':ann})

curr_course="hh"
curr_cid="hhh"
def courseInfo(request,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    course=List.objects.get(pk=cid)
    global curr_course
    global curr_cid
    curr_course=course
    curr_cid=cid
    i=instructors.objects.filter(course=course)
    l=links.objects.filter(course=course)
    ass=assignments.objects.filter(course=course)
    ann=announcements.objects.filter(course=course)
    topics=topic.objects.filter(course=course)
    return render(request, 'courseInfo.html', {'course':course,'topics':topics,'i':i,'l':l,'ass':ass,'ann':ann,'cid':cid})

def Raccess(request,cid,rtype):
    course=List.objects.get(pk=cid)
    try:
        a=resAccess.objects.get(email=request.user.username,rType=rtype,course=course.item,date=datetime.datetime.now())
        a.sum_click+=1
        a.save()
    except:
        a=resAccess(name=request.user.first_name+' '+request.user.last_name,email=request.user.username,rType=rtype,course=course.item)
        a.save()
    return HttpResponse('')

def updatecred(request,cid):
    if request.method=='POST':
        newcred=request.POST['Credits']
        cr=float(newcred)
        curr_course=List.objects.get(pk=cid)
        curr_course.cred=cr
        curr_course.save()
        return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')

def editsyll(request,cid):
    if request.method=='POST':
        newsyll=request.POST['new']
        curr_course=List.objects.get(pk=cid)
        curr_course.syllabus=newsyll
        curr_course.save()
        return JsonResponse({'neww':model_to_dict(curr_course)},status=200)
        #return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')

def editdesc(request,cid):
    if request.method=='POST':
        newdesc=request.POST['new']
        curr_course=List.objects.get(pk=cid)
        curr_course.desc=newdesc
        curr_course.save()
        return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')
    
def addTopic(request,cid):
    if request.method=='POST':
        new=request.POST['topic']
        curr_course=List.objects.get(pk=cid)
        it=topic(name=new,course=curr_course)
        it.save()
        return JsonResponse({'neww':model_to_dict(it)},status=200)
    else:
        return redirect('Link2')

def delTopic(request,tid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    it=topic.objects.get(pk=tid)
    it.delete()
    return JsonResponse({'result':'ok'},status=200)

def addInst(request,cid):
    if request.method=='POST':
        newInst=request.POST['Instructor']
        curr_course=List.objects.get(pk=cid)
        it=instructors(inst=newInst,course=curr_course)
        it.save()
        return JsonResponse({'neww':model_to_dict(it)},status=200)
        #return HttpResponse('')
        #return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')

def delInst(request,instid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    it=instructors.objects.get(pk=instid)
    it.delete()
    return JsonResponse({'result':'ok'},status=200)
    #return redirect('courseInfo',cid=curr_cid)

def addLink(request,cid):
    if request.method=='POST':
        newLink=request.POST['Link']
        topic1=request.POST['topic_']
        curr_course=List.objects.get(pk=cid)
        it=links(link=newLink,topic=topic1,course=curr_course)
        it.save()
        return JsonResponse({'neww':model_to_dict(it)},status=200)
        #return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')

def delLink(request,linkid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    it=links.objects.get(pk=linkid)
    it.delete()
    return JsonResponse({'result':'ok'},status=200)
    #return redirect('courseInfo',cid=curr_cid)

def addannc(request,cid):
    if request.method=='POST':
        newannc=request.POST['Announcement']
        curr_course=List.objects.get(pk=cid)
        it=announcements(annc=newannc,course=curr_course)
        it.save()
        size=announcements.objects.filter(course=curr_course).count()
        return JsonResponse({'neww':model_to_dict(it),'size':size},status=200)
    else:
        return redirect('Link2')

def delannc(request,anncid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    it=announcements.objects.get(pk=anncid)
    it.delete()
    return JsonResponse({'result':'ok'},status=200)

def addassign(request,cid):
    if request.method=='POST':
        file = request.FILES['file']
        name1=request.POST['name']
        topic1=request.POST['topic_']
        curr_course=List.objects.get(pk=cid)
        a=assignments(name=name1,assign=file,topic=topic1,course=curr_course)
        a.save()
        return JsonResponse({'fileid':a.id,'name':a.name,'fileurl':a.assign.url,'topic':a.topic},status=200)
        #return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')
    
def delassign(request,assid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    a=assignments.objects.get(pk=assid)
    a.delete()
    return JsonResponse({'result':'ok'},status=200)
    #return redirect('courseInfo',cid=curr_cid)
    
stodel="hh"
curr_sl="hh"
studentid="hh"

def studlist(request,sidd):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    item=List.objects.get(pk=sidd)
    global curr_sl
    global studentid
    studentid=sidd
    curr_sl=item
    sl=studList.objects.filter(course=item)
    return render(request, 'Link2_studlist.html', {'sl':sl,'sidd':sidd})

def addstudgetid(request,list_id):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    return render(request, 'Link2_addstud.html', {'list_id':list_id})

def addstud(request,list_id):
    if request.method=='POST':
        crse=List.objects.get(pk=list_id)
        name=request.POST['message']
        name=name.replace("\r",",")
        name=name.replace("\n","")
        namelist=name.split(',')
        for i in namelist:
            if studList.objects.filter(email=i,course=crse).exists():
                print('Already exists: ',i)
            else:
                it=studList(email=i,course=crse)
                it.save()
        subject = 'Course Invite'
        message = 'This is an invite for the course: '+crse.item+'\n Click the below link to go to the registeration page \n \n http://sunvir.pythonanywhere.com/courses/ '
        email_from = settings.EMAIL_HOST_USER
        #for visualization:
        #recipient_list = ['sunvirsingh72@gmail.com',]
        #actual code:
        recipient_list = namelist
        send_mail(subject,message,email_from,recipient_list,fail_silently=False)
        messages.success(request,('Email Invite sent successfully!'))
        return render(request, 'Link2_addstud.html', {'name':name,'list_id':list_id})
    else:
        return redirect('Link2')

    
def deleteStud(request,stud,sidd):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    it=studList.objects.get(pk=stud)
    it.delete()
    return JsonResponse({'result':'ok'},status=200)
    #return redirect('studlist',sidd=sidd)

def studR(request):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    srs=studRecords.objects.all()
    uniqcrs=List.objects.all().values_list('item', flat=True)
    crsfreq=[]
    try:
        last_n = srs.order_by('-id')[:10]
    except:
        last_n = ras.order_by('-id')
    for i in uniqcrs:
        crsfreq.append(srs.filter(course=i).count())

    return render(request, 'studRecords.html', {'rows':srs.count(),'srs':last_n,'uniqcrs':list(uniqcrs),'crsfreq':crsfreq})

def RaccessT(request):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    ras=resAccess.objects.all()
    try:
        last_n = ras.order_by('-id')[:10]
    except:
        last_n = ras.order_by('-id')
    rTypeSums={'rows':ras.count(),'ras':last_n,'link':0,'assignment':0,'questionnaire':0}
    for i in ras:
        rTypeSums[i.rType]+=i.sum_click
    return render(request, 'RaccessT.html', rTypeSums)
    
def RaTdown(request):
    #print('in')
    allobj=resAccess.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resource_access.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Email','Course','Resource Type','Date','Last Time','Click sum'])

    for obj in allobj:
        writer.writerow([obj.name,obj.email,obj.course,obj.rType,obj.date,str(obj.time.hour) +':'+str(obj.time.minute),obj.sum_click])

    return response

def CaTdown(request):
    allobj=studRecords.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="course_access.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Email','Course','Date and Time'])

    for obj in allobj:
        writer.writerow([obj.name,obj.email,obj.course,obj.DT])

    return response

def deleteSR(request,sr):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    item=studRecords.objects.get(pk=sr)
    item.delete()
    return redirect('studR')

def delete(request,list_id):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    item=List.objects.get(pk=list_id)
    item.delete()
    return redirect('Link2')

def edit(request,cid):
    if request.method=='POST':
        newit=request.POST['item']
        curr_course=List.objects.get(pk=cid)
        curr_course.item=newit
        curr_course.save()
        return redirect('courseInfo',cid=curr_cid)
    else:
        return redirect('Link2')

def quesRO(request,curr_c):
    if not request.user.is_authenticated:
        return redirect('Link2')
    #return HttpResponse('safe')
    curr_crse=List.objects.get(pk=curr_c)
    all_q=questr.objects.filter(course=curr_crse)
    return render(request, 'addqRO.html', {'all_q':all_q,'cr_crseid':curr_c})

def quesr(request,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    curr_course=List.objects.get(pk=cid)
    if request.method=='POST':
        newq=request.POST['item']
        type1=request.POST['type']
        if type1=='Test':
            hrs1=request.POST['hrs']
            min1=request.POST['min']
            a=questr(name=newq,DT=datetime.datetime.now(),time=hrs1+':'+min1,qtype=type1,course=curr_course)
            a.save()
        else:
            a=questr(name=newq,DT=datetime.datetime.now(),qtype=type1,course=curr_course)
            a.save()
        all_q=questr.objects.filter(course=curr_course)
        return render(request, 'addq.html', {'all_q':all_q,'cid':cid})
    else:
        all_q=questr.objects.filter(course=curr_course)
        return render(request, 'addq.html', {'all_q':all_q,'cid':cid})

def delquesr(request,pk1,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    a=questr.objects.get(pk=pk1)
    a.delete()
    return redirect('quesr',cid=cid)
'''
def qnRO(request,pk1,cr_crseid):
    if not request.user.is_authenticated:
        return redirect('Link2')
    curr_q=questr.objects.get(pk=pk1)
    course=List.objects.get(pk=cr_crseid)
    if request.method == 'POST':
        n=ques.objects.filter(qnr=curr_q).count()
        all_qns=ques.objects.filter(qnr=curr_q)
        na=0
        correct=0
        wrong=0
        score=0
        lst=[]
        for i in range(0,n):
            if all_qns[i].isradio:
                try:
                    if all_qns[i].correct == request.POST[str(i)]:
                        correct+=1
                        score+=all_qns[i].marks
                    else:
                        wrong+=1
                        score-=all_qns[i].neg
                except:
                    na+=1
            else:
                c=','.join(request.POST.getlist(str(i)+'[]'))
                if c=='':
                    na+=1
                elif all_qns[i].correct == c:
                    correct+=1
                    score+=all_qns[i].marks
                else:
                    wrong+=1
                    score-=all_qns[i].neg
        if curr_q.qtype=='Test':
            if attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                messages.warning(request,('You have already submitted this Test!'))
                return redirect('quesRO',cr_crseid)
            else:
                a=attempt(name=request.user.first_name,email=request.user.username,DT=datetime.datetime.now(),na=na,correct=correct,wrong=wrong,score=score,qnr=curr_q)
                a.save()
                messages.success(request,('Your Answers have been recorded successfully!'))
                return redirect('Link2')
        else:
            a=attempt(name=request.user.first_name,email=request.user.username,DT=datetime.datetime.now(),na=na,correct=correct,wrong=wrong,score=score,qnr=curr_q)
            a.save()
            messages.success(request,('Your Answers have been recorded successfully!'))
            return redirect('Link2')

#---------------------------------------------------------------------------------------------------------------------If reques is not POST:
    try:
        if studList.objects.filter(email=request.user.username,stat=True,course=course).exists():
            if curr_q.qtype=='Test':
                if attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                    messages.warning(request,('You have already submitted this Test!'))
                    return redirect('quesRO',cr_crseid)

            #--------------------------------------------------------------------------------------------------resAccess
            course=List.objects.get(pk=cr_crseid)
            try:
                a=resAccess.objects.get(email=request.user.username,rType='questionnaire',course=course.item,date=datetime.datetime.now())
                a.sum_click+=1
                a.save()
            except:
                a=resAccess(name=request.user.first_name+' '+request.user.last_name,email=request.user.username,rType='questionnaire',course=course.item)
                a.save()
            #---------------------------------------------------------------------------------------------------
            
            all_q=ques.objects.filter(qnr=curr_q)
            return render(request, 'qnRO.html', {'pk1':pk1,'all_q':all_q,'curr_q':curr_q,'cr_crseid':cr_crseid})
        else:
            messages.warning(request,('Please register for the course to attempt this questionnaire!'))
            return redirect('quesRO',cr_crseid)
    except:
        if studList.objects.filter(email=request.user.username,stat=True,course=course).exists():
            if curr_q.qtype=='Test':
                if attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                    messages.warning(request,('You have already submitted this Test!'))
                    return redirect('quesRO',cr_crseid)
            return render(request, 'qnRO.html', {'pk1':pk1,'curr_q':curr_q,'cr_crseid':cr_crseid})
        else:
            messages.warning(request,('Please register for the course to attempt this questionnaire!'))
            return redirect('quesRO',cr_crseid)
'''

def qnRO(request,pk1,cr_crseid):
    if not request.user.is_authenticated:
        return redirect('Link2')
    curr_q=questr.objects.get(pk=pk1)
    course=List.objects.get(pk=cr_crseid)
    if request.method == 'POST':
        if curr_q.qtype=='Test':
            #This part is for: if user goes back and tries to submit again
            if qnr_attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                messages.warning(request,('You have already submitted this Test!'))
                return redirect('quesRO',cr_crseid)
        a=qnr_attempt(name=request.user.first_name,email=request.user.username,DT=datetime.datetime.now(),qnr=curr_q)
        a.save()
        n=ques.objects.filter(qnr=curr_q).count()
        all_qns=ques.objects.filter(qnr=curr_q)
        #na=0
        #correct=0
        #wrong=0
        score=0
        lst=[]
        for i in range(0,n):
            if all_qns[i].isradio:
                try:
                    if all_qns[i].correct == request.POST[str(i)]:
                        #correct+=1
                        b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=1)
                        b.save()
                        score+=all_qns[i].marks
                    else:
                        b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=2)
                        b.save()
                        #wrong+=1
                        score-=all_qns[i].neg
                except:
                    b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=3)
                    b.save()
                    #na+=1
            else:
                c=','.join(request.POST.getlist(str(i)+'[]'))
                if c=='':
                    #na+=1
                    b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=3)
                    b.save()
                elif all_qns[i].correct == c:
                    #correct+=1
                    b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=1)
                    b.save()
                    score+=all_qns[i].marks
                else:
                    b=qn_attempt(qnr_attempt=a,ques=all_qns[i],stat=2)
                    b.save()
                    #wrong+=1
                    score-=all_qns[i].neg

        a.score=score
        a.save()
        messages.success(request,('Your Answers have been recorded successfully!'))
        return redirect('Link2')

#---------------------------------------------------------------------------------------------------------------------If reques is not POST:
    try:
        if studList.objects.filter(email=request.user.username,stat=True,course=course).exists():
            if curr_q.qtype=='Test':
                if qnr_attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                    messages.warning(request,('You have already submitted this Test!'))
                    return redirect('quesRO',cr_crseid)

            #--------------------------------------------------------------------------------------------------resAccess
            course=List.objects.get(pk=cr_crseid)
            try:
                a=resAccess.objects.get(email=request.user.username,rType='questionnaire',course=course.item,date=datetime.datetime.now())
                a.sum_click+=1
                a.save()
            except:
                a=resAccess(name=request.user.first_name+' '+request.user.last_name,email=request.user.username,rType='questionnaire',course=course.item)
                a.save()
            #---------------------------------------------------------------------------------------------------
            
            all_q=ques.objects.filter(qnr=curr_q)
            return render(request, 'qnRO.html', {'pk1':pk1,'all_q':all_q,'curr_q':curr_q,'cr_crseid':cr_crseid})
        else:
            messages.warning(request,('Please register for the course to attempt this questionnaire!'))
            return redirect('quesRO',cr_crseid)
    except:
        if studList.objects.filter(email=request.user.username,stat=True,course=course).exists():
            if curr_q.qtype=='Test':
                if qnr_attempt.objects.filter(qnr=curr_q,email=request.user.username).exists():
                    messages.warning(request,('You have already submitted this Test!'))
                    return redirect('quesRO',cr_crseid)
            return render(request, 'qnRO.html', {'pk1':pk1,'curr_q':curr_q,'cr_crseid':cr_crseid})
        else:
            messages.warning(request,('Please register for the course to attempt this questionnaire!'))
            return redirect('quesRO',cr_crseid)


def qn(request,pk1,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    curr_q=questr.objects.get(pk=pk1)
    curr_c=List.objects.get(pk=cid)
    topics=topic.objects.filter(course=curr_c)
    if request.method=='POST':
        quesn=request.POST['item']
        op1=request.POST['op1']
        op2=request.POST['op2']
        op3=request.POST['op3']
        op4=request.POST['op4']
        op5=request.POST['op5']
        op6=request.POST['op6']
        c1=request.POST.getlist('correct[]')
        marks1=request.POST['marks']
        neg1=request.POST['neg']
        topic1=request.POST['topic_']
        level=request.POST['level']
        if len(c1)==1:
            a=ques(ques=quesn,opt1=op1,opt2=op2,opt3=op3,opt4=op4,opt5=op5,opt6=op6,correct=c1[0],topic=topic1,level=level,marks=marks1,neg=neg1,qnr=curr_q)
            a.save()
        else:
            c=','.join(c1)
            a=ques(ques=quesn,opt1=op1,opt2=op2,opt3=op3,opt4=op4,opt5=op5,opt6=op6,correct=c,topic=topic1,level=level,isradio=False,marks=marks1,neg=neg1,qnr=curr_q)
            a.save()
        all_q=ques.objects.filter(qnr=curr_q)
        return render(request, 'qn.html', {'cid':cid,'pk1':pk1,'all_q':all_q,'curr_q':curr_q,'topics':topics})
    else:
        try:
            all_q=ques.objects.filter(qnr=curr_q)
            return render(request, 'qn.html', {'cid':cid,'pk1':pk1,'all_q':all_q,'curr_q':curr_q,'topics':topics})
        except:
            return render(request, 'qn.html', {'cid':cid,'pk1':pk1,'curr_q':curr_q,'topics':topics})

def bulkqn(request,pk1,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    curr_q=questr.objects.get(pk=pk1)
    if request.method=='POST':
        try:
            file = request.FILES['file']
            df=pd.read_csv(file,keep_default_na=False)
            r=df.shape[0]
            #checking if rows>300
            if (r>300):
                messages.warning(request,('Error! Maximum 300 questions allowed per upload'))
                try:
                    all_q=ques.objects.filter(qnr=curr_q)
                    return render(request, 'qn.html', {'pk1':pk1,'all_q':all_q,'curr_q':curr_q})
                except:
                    return render(request, 'qn.html', {'pk1':pk1,'curr_q':curr_q})
            #if not:
            df=df.iloc[:,:].values
            print('here')
            for i in range(0,r):
                print('in')
                if len(df[i][7])==1:
                    a=ques(ques=df[i][0],opt1=df[i][1],opt2=df[i][2],opt3=df[i][3],opt4=df[i][4],opt5=df[i][5],opt6=df[i][6],correct=df[i][7],marks=df[i][8],neg=df[i][9],level=int(df[i][10]),topic=df[i][11],qnr=curr_q)                
                    a.save()
                else:
                    a=ques(ques=df[i][0],opt1=df[i][1],opt2=df[i][2],opt3=df[i][3],opt4=df[i][4],opt5=df[i][5],opt6=df[i][6],correct=df[i][7],marks=df[i][8],neg=df[i][9],level=df[i][10],topic=df[i][11],isradio=False,qnr=curr_q)                
                    a.save()
            print('here')
            #all_q=ques.objects.filter(qnr=curr_q)
            return redirect('qn',pk1=pk1,cid=cid)
            #return render(request, 'qn.html', {'cid':cid,'pk1':pk1,'all_q':all_q,'curr_q':curr_q,'topics':topics})
        except:
            messages.warning(request,('Error! Please look at the sample file to make sure your file meets the requirements'))
            return redirect('qn',pk1=pk1,cid=cid)
    else:
        return redirect('qn',pk1=pk1,cid=cid)


def delqn(request,pk1,qpk,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    #if request.method=='POST':
    a=ques.objects.get(pk=pk1)
    a.delete()
    return redirect('qn',pk1=qpk,cid=cid)
    #return redirect('Link2')

def email(request,pk1,cid):
    course=List.objects.get(pk=cid)
    quesr=questr.objects.get(pk=pk1)
    subject = 'Reminder for Questionnaire'
    message = 'This is to remind you that you have not yet attempted the '+quesr.qtype+' quesstionnaire: '+quesr.name+', for the course: '+course.item
    email_from = settings.EMAIL_HOST_USER
    #for visualization:
    recipient_list = ['sunvirsingh72@gmail.com',]
    #actual code:
    '''
    regstuds=studList.objects.filter(course=course,stat=True)
    uniqatt=attempt.objects.filter(qnr=quesr).values_list('email', flat=True).distinct()
    notyet=regstuds
    for i in range(0,len(uniqatt)):
        notyet=notyet.exclude(email=uniqatt[i])
    mailTo=list(notyet.values_list('email', flat=True))
    recipient_list = mailTo
    '''
    send_mail(subject,message,email_from,recipient_list,fail_silently=False)
    messages.success(request,('Email Reminder sent successfully!'))
    return redirect('qnr_attempts',pk1=pk1,cid=cid)


def qnr_attempts(request,pk1,cid):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    #PUT THIS IN TRY!!
    curr_q=questr.objects.get(pk=pk1)
    curr_crse=List.objects.get(pk=cid)
    try:
        attempts=qnr_attempt.objects.filter(qnr=curr_q)
        mean=attempts.aggregate(Avg('score'))
        regstuds=studList.objects.filter(course=curr_crse,stat=True)
        uniqatt=attempts.values_list('email', flat=True).distinct()
        notyet=regstuds
        for i in range(0,len(uniqatt)):
            notyet=notyet.exclude(email=uniqatt[i])
        sendmail=",".join(list(notyet.values_list('email', flat=True)))
        return render(request, 'attempts_.html', {'pk1':pk1,'cid':cid,'curr_q':curr_q,'curr_crse':curr_crse,'attempts':attempts,'mean':mean['score__avg'],'regstuds':regstuds,'notyet':notyet,'sendmail':sendmail})
    except:
        return render(request, 'attempts_.html', {'curr_q':curr_q})

def qn_attempts(request,pk1):
    if not request.user.is_authenticated or not request.user.profile.ifTeacher:
        return redirect('Link2')
    curr_att=qnr_attempt.objects.get(pk=pk1)
    q_attempts=qn_attempt.objects.filter(qnr_attempt=curr_att)
    jdict={'quesns':[],'ans':[]}
    for i in q_attempts:
        jdict['quesns'].append(i.ques.ques)
        jdict['ans'].append(i.stat)
    return JsonResponse(jdict,status=200)
    return render(request, 'attempts_q.html', {'q_attempts':q_attempts,'name':curr_att.name,'qnr':curr_att.qnr.name})


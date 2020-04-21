from django.db import models

class List(models.Model):
    item=models.CharField(max_length=200)
    desc=models.TextField(default='Edit description here')
    cred=models.FloatField(default=float(0.0))
    syllabus=models.TextField(default='Edit syllabus here')
    def __str__(self):
        return self.item + ' | ' + ' | ' +self.desc + ' | ' +self.syllabus

class topic(models.Model):
    name=models.CharField(max_length=200)
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class links(models.Model):
    link=models.CharField(max_length=400)
    topic=models.CharField(max_length=200,default="None")
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.link

class instructors(models.Model):
    inst=models.CharField(max_length=200)
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.inst

class assignments(models.Model):
    name=models.CharField(max_length=200,default='test')
    assign=models.FileField(upload_to='assign/')
    topic=models.CharField(max_length=200,default="None")
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.assign.delete()
        super().delete(*args, **kwargs)

class announcements(models.Model):
    annc=models.TextField()
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.annc

class studList(models.Model):
    name=models.CharField(max_length=200,default='NA')
    email=models.CharField(max_length=200)
    stat=models.BooleanField(default=False)
    course=models.ForeignKey(List,on_delete=models.CASCADE)
    def __str__(self):
        return self.email

class studDetails(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    gender=models.CharField(max_length=10)
    regDate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+' | '+self.email
    
class resAccess(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    rType=models.CharField(max_length=50)
    course=models.CharField(max_length=200)
    date=models.DateField(auto_now=True)
    time=models.TimeField(auto_now=True)
    sum_click=models.IntegerField(default=1)
 
    def __str__(self):
        return self.name+' | '+self.rType+' | '+str(self.sum_click)


class studRecords(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    course=models.CharField(max_length=200)
    DT=models.DateTimeField()

    def __str__(self):
        return self.email+' | '+self.course
    
class questr(models.Model):
    name=models.CharField(max_length=200)
    DT=models.DateTimeField()
    time=models.CharField(max_length=10,default='NA')
    qtype=models.CharField(max_length=15,default='h')
    course=models.ForeignKey(List,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class ques(models.Model):
    ques=models.TextField()
    opt1=models.CharField(max_length=150)
    opt2=models.CharField(max_length=150)
    opt3=models.CharField(max_length=150)
    opt4=models.CharField(max_length=150)
    opt5=models.CharField(max_length=150)
    opt6=models.CharField(max_length=150)
    correct=models.CharField(max_length=12)
    marks=models.FloatField(default=float(1.0))
    neg=models.FloatField(default=float(0.0))
    isradio=models.BooleanField(default=True)
    topic=models.CharField(max_length=200,default="None")
    level=models.IntegerField(default=1)
    qnr=models.ForeignKey(questr,on_delete=models.CASCADE)

    def __str__(self):
        return self.ques

class attempt(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    DT=models.DateTimeField()
    na=models.CharField(max_length=5)
    correct=models.CharField(max_length=5)
    wrong=models.CharField(max_length=5)
    score=models.FloatField(default=float(0.0))
    qnr=models.ForeignKey(questr,on_delete=models.CASCADE)
        
    def __str__(self):
        return self.name

class qnr_attempt(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    DT=models.DateTimeField()
    score=models.FloatField(default=float(0.0))
    qnr=models.ForeignKey(questr,on_delete=models.CASCADE)

    def __str__(self):
        return self.email+' | '+self.qnr

class qn_attempt(models.Model):
    #email=models.CharField(max_length=200)
    #quesnr=models.ForeignKey(questr,on_delete=models.CASCADE)
    qnr_attempt=models.ForeignKey(qnr_attempt,on_delete=models.CASCADE)
    ques=models.ForeignKey(ques,on_delete=models.CASCADE)
    #something.ques.ques
    stat=models.IntegerField()

    def __str__(self):
        return self.stat


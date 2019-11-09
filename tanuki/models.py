from django.db import models

class Photo(models.Model):
    userNo = models.IntegerField()
    FileName = models.CharField(max_length=40,default='none')
    file = models.ImageField(upload_to='tanuki')
    FilePath = models.CharField(max_length=100,default='none')
    cate = models.CharField(max_length=30,default='other')
    sub = models.CharField(max_length=30,default='other')
    color = models.CharField(max_length=30,null=True)

class Account(models.Model):
    name = models.CharField(max_length=100,default='none')
    sex = models.CharField(max_length=2,default='none')
    age = models.IntegerField()
    type = models.CharField(max_length=30,default='none')

class BlackList(models.Model):
    sub1 = models.CharField(max_length=30)
    sub2 = models.CharField(max_length=30)

class Codenate(models.Model):
    sub1 = models.CharField(max_length=30,null=True)
    sub2 = models.CharField(max_length=30,null=True)
    sub3 = models.CharField(max_length=30,null=True)
    sub4 = models.CharField(max_length=30,null=True)
    sub5 = models.CharField(max_length=30,null=True)


    


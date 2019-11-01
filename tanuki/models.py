from django.db import models

class Photo(models.Model):
    userNo = models.IntegerField()
    FileName = models.CharField(max_length=40,primary_key=True)
    file = models.ImageField(upload_to='tanuki')
    FilePath = models.CharField(max_length=100,default='none')
    cate = models.CharField(max_length=10,default='other')
    sub = models.CharField(max_length=10,default='other')
    color = models.CharField(max_length=10,null=True)

class Account(modesl.Model):
    name = models.CharField(max_length=100,default='none')
    sex = models.CharField(max_length=2)
    age = models.IntegerField()
    type = models.CharField(max_length=10,default='none')

    


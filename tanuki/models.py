from django.db import models

class Photo(models.Model):
    userNo = models.IntegerField()
    FileName = models.CharField(max_length=40,default='none')
    file = models.ImageField(upload_to='tanuki')
    FilePath = models.CharField(max_length=100,default='none')
    cate = models.CharField(max_length=30,default='other')
    sub = models.ForeignKey(Sub_type_value,on_delete=models.CASCADE)
    color = models.ForeignKey(Color_type_value,on_delete=models.CASCADE)

class Account(models.Model):
    name = models.CharField(max_length=100,default='none')
    sex = models.CharField(max_length=10,default='none')
    age = models.IntegerField()
    type = models.CharField(max_length=30,default='none')

class BlackList(models.Model):
    sub1 = models.CharField(max_length=30)
    sub2 = models.CharField(max_length=30)

class Sub_type_value(models.Model):
    sub = models.CharField(max_length=30)
    type1 = models.CharField(max_length=30,null=True)
    type2 = models.CharField(max_length=30,null=True)

class Color_type_value(models.Model):
    color = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


class Codenate(models.Model):
    sub1 = models.CharField(max_length=30,null=True)
    sub2 = models.CharField(max_length=30,null=True)
    sub3 = models.CharField(max_length=30,null=True)
    sub4 = models.CharField(max_length=30,null=True)
    sub5 = models.CharField(max_length=30,null=True)


    


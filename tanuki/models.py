from django.db import models

class Sub_type_value(models.Model):
    class Meta:
        db_table = 'Sub_type_value'

    sub = models.CharField(verbose_name='サブ',max_length=30)
    type1 = models.CharField(verbose_name='タイプ1',max_length=30,null=True)
    type2 = models.CharField(verbose_name='タイプ2',max_length=30,null=True)

    def __str__(self):
        return self.sub

class Color_type_value(models.Model):
    class Meta:
        db_table = 'Color_type_value'

    color = models.CharField(verbose_name='色',max_length=30)
    type = models.CharField(verbose_name='タイプ',max_length=30)
    
    def __str__(self):
        return self.color

class Photo(models.Model):
    class Meta:
        db_table = 'Photo'

    userNo = models.IntegerField(verbose_name='ユーザーNo')
    FileName = models.CharField(verbose_name='ファイル名',max_length=40,default='none')
    file = models.ImageField(verbose_name='ファイル',upload_to='tanuki')
    FilePath = models.CharField(verbose_name='ファイルパス',max_length=100,default='none')
    cate = models.CharField(verbose_name='カテゴリ',max_length=30,default='other')
    sub = models.CharField(verbose_name='サブカテゴリ',max_length=30,default='other')
    color = models.CharField(verbose_name='色',max_length=30,default='other')    
    sub_type_value = models.ForeignKey(Sub_type_value,on_delete=models.CASCADE)
    color_type_value = models.ForeignKey(Color_type_value,on_delete=models.CASCADE)
    def __str__(self):
        return 'userNo:'+ self.userNo + ' FileName:' + self.FileName + ' sub:' + self.sub
class Account(models.Model):
    class Meta:
        db_table = 'Account'

    name = models.CharField(verbose_name='名前',max_length=100,default='none')
    sex = models.CharField(verbose_name='性別',max_length=10,default='none')
    age = models.IntegerField(verbose_name='年齢')
    type = models.CharField(verbose_name='タイプ',max_length=30,default='none')

    def __str__(self):
        return self.name

class BlackList(models.Model):
    class Meta:
        db_table = 'BlackList'

    sub1 = models.CharField(verbose_name='サブ１',max_length=30)
    sub2 = models.CharField(verbose_name='サブ２',max_length=30)

    def __str__(self):
        return 'sub1:' + self.sub1 + ' sub2:' + self.sub2

class Codenate(models.Model):
    class Meta:
        db_table = 'Codnate'

    sub1 = models.CharField(verbose_name='サブ1',max_length=30,null=True)
    sub2 = models.CharField(verbose_name='サブ2',max_length=30,null=True)
    sub3 = models.CharField(verbose_name='サブ3',max_length=30,null=True)
    sub4 = models.CharField(verbose_name='サブ4',max_length=30,null=True)
    sub5 = models.CharField(verbose_name='サブ5',max_length=30,null=True)

    def __str__(self):
        return 'sub1:' + self.sub1 + ' sub2:' + sub2 + ' sub3:' + self.sub3 + ' sub4:' + self.sub4 + ' sub5:' + self.sub5

    


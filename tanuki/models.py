from django.db import models

class Photo_one(models.Model):
    class Meta:
        db_table = 'Photo_one'
    
    photo = models.ImageField(verbose_name='画像',upload_to='tanuki')

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
    dress_value = models.IntegerField(verbose_name='ドレス率')
    casual_value = models.IntegerField(verbose_name='カジュアル率')
    simple_value = models.IntegerField(verbose_name='シンプル率')
    vol = models.CharField(verbose_name='勢い',max_length=30)
    tag = models.CharField(verbose_name='タグ1',max_length=20,null=True)
    tag2 = models.CharField(verbose_name='タグ2',max_length=20,null=True)
    tag3 = models.CharField(verbose_name='タグ3',max_length=20,null=True)
    tag4 = models.CharField(verbose_name='タグ4',max_length=20,null=True)
    def __str__(self):
        return 'userNo:'+ str(self.userNo) + ' FileName:' + self.FileName + ' sub:' + self.sub
class Account(models.Model):
    class Meta:
        db_table = 'Account'

    name = models.CharField(verbose_name='名前',max_length=100,default='none')
    sex = models.CharField(verbose_name='性別',max_length=10,default='none')
    age = models.IntegerField(verbose_name='年齢')
    type = models.CharField(verbose_name='タイプ',max_length=30,default='none')

    def __str__(self):
        return self.name

class Codnate_sample(models.Model):
    class Meta:
        db_table = 'Codnate'
    sample = models.ImageField(verbose_name='サンプルパス',upload_to='sample')
    sub1 = models.CharField(verbose_name='サブ1',max_length=30,null=True)
    sub2 = models.CharField(verbose_name='サブ2',max_length=30,null=True)
    sub3 = models.CharField(verbose_name='サブ3',max_length=30,null=True)
    sub4 = models.CharField(verbose_name='サブ4',max_length=30,null=True,blank=True)
    sub5 = models.CharField(verbose_name='サブ5',max_length=30,null=True,blank=True)

   

class Codnate_type_temp(models.Model):
    class Meta:
        db_table = 'Codnate_type_temp'
    
    code_type = models.CharField(verbose_name='タイプ',max_length=30)
    dress_value = models.IntegerField(verbose_name='ドレス率')
    casual_value = models.IntegerField(verbose_name='カジュアル率')
    simple_value = models.IntegerField(verbose_name='シンプル率')
    tag1 = models.CharField(verbose_name='タグ1',max_length=30,null=True)
    tag2 = models.CharField(verbose_name='タグ2',max_length=30,null=True)
    tag3 = models.CharField(verbose_name='タグ3',max_length=30,null=True)
    tag4 = models.CharField(verbose_name='タグ4',max_length=30,null=True)
    vol = models.CharField(verbose_name='勢い',max_length=30)

    
class Good_Codnate(models.Model):
    class Meta:
        db_table = 'Good_Codnate'
    
    userNo = models.IntegerField(verbose_name='ユーザーNO')

class Bad_Codnate(models.Model):
    class Meta:
        db_table = 'Bad_Codnate'
    
    userNo = models.IntegerField(verbose_name='ユーザーNO')
    tops_path = models.CharField(verbose_name='トップスパス',max_length=100)
    botoms_path = models.CharField(verbose_name='ボトムスパス',max_length=100)
    shoese_path = models.CharField(verbose_name='シューズパス',max_length=100)


    


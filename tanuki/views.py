from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json
from django.db import models
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.shortcuts import get_current_site
import re
from django.core.files import File
from django.db.models import Max,Sum
from .forms import PhotoForm,AccountForm,PhotoOneForm
from django.views.decorators.csrf import csrf_exempt
import random
from django.db.models import Q

#テスト用
def index(request):
    return HttpResponse("hallo django")

def get_photo_count(request):
    userNo = request.GET.get('UserNo')
    user_photo_all = models.QuerySet(Photo).filter(userNo=userNo)
    tops_count = user_photo_all.filter(cate='tops').count()
    botoms_count = user_photo_all.filter(cate='botoms').count()
    shoese_count = user_photo_all.filter(cate='shoese').count()

   

    return HttpResponse(str(tops_count)+','+str(botoms_count)+','+str(shoese_count))
@csrf_exempt
def newAccount(request):
    if request.method == 'GET':
        return HttpResponse('a')
    try:
        form = AccountForm(request.POST,request.FILES)
        name = request.POST['name']
        sex  = request.POST['sex']
        age  = int(request.POST['age'])
        type = request.POST['type']
        
        ac = Account(name=name,sex=sex,age=age,type=type)
        ac.save()
        UserNo = models.QuerySet(Account).all().aggregate(Max('id'))
        
        return HttpResponse(str(UserNo['id__max']))
    except Exception:
        return HttpResponse('totyudeerror')
        
#画像のPOST用　userNoとファイルとファイル名がセットで来る
@csrf_exempt
def imgInDB(request):
    
    #GETだった場合
    if request.method == 'GET':
        return HttpResponse("error")
    
    try:
        #ファイルが入っているか確認
        if request.FILES == None:
            HttpResponse('error')
        #アップロードされたファイルを変数に格納
        print(request.POST)
        form = PhotoForm(request.POST,request.FILES)
        if not form.is_valid():
            return HttpResponse("error")
            raise ValueError('invalid form')        
        filename = str(form.cleaned_data['image'])
        userNo = re.split('_',filename)
        userNo = int(userNo[0])
        cate = request.POST['cate']
        sub = request.POST['sub']
        color = request.POST['color']
        dress = int(request.POST['dress'])
        casual = int(request.POST['casual'])
        simple = int(request.POST['simple'])
        tag1 = request.POST['tag1']
        tag2 = request.POST['tag2']
        tag3 = request.POST['tag3']
        tag4 = request.POST['tag4']
        vol = request.POST['vol']
        print('user->'+str(userNo))
        #画像をDBに登録
        photo = Photo(userNo=userNo,FileName=filename,file=form.cleaned_data['image'],
                      cate=cate,sub=sub,color=color,dress_value=dress,casual_value=casual,simple_value=simple,
                      tag=tag1,tag2=tag2,tag3=tag3,tag4=tag4,vol=vol)
        photo.save()
        #画像のパスを作成
        #飛んできたリクエストからURLを取得
        current_site = get_current_site(request)
        #URLのドメインのみを取得
        domain = current_site.domain
        #画像のURLを作成
        download_url = '{0}://{1}{2}'.format(
        request.scheme,
        domain,
        photo.file.url,
        )
        #DBの画像のURLを更新
        photo = models.QuerySet(Photo)
        photo_obj = photo.filter(FileName=filename).first()
        photo_obj.FilePath = download_url
        photo_obj.save()
        #URLを文字列として返してあげる
        return HttpResponse("File Up load Complete")

    except Exception:
        #画像じゃないとき、または例外発生
        return HttpResponse('totyu de error')

@csrf_exempt
def imgChageInfo(request):
    if request.method == 'GET':
        return HttpResponse('error')

    else:
        try:
            
            return HttpResponse('info change compleate')
        except Exception:
            return HttpResponse('totyuu de erorr')

@csrf_exempt
def img_delete(request):
    if request.method == "GET":
        return HttpResponse("error")
    try:
        path = request.POST["filePath"]
        Photo.objects.filter(FilePath=path).delete()
        return HttpResponse("Delete compleate")
    except Exception:
        return HttpResponse("totyu de error")
#画像のGET専用
def getImage(request):
    #それぞれを抽出(UserNo以外配列)
    userNo = request.GET.get('UserNo')
    cate = request.GET.get('cate')
    sub = request.GET.get('sub')
    color = request.GET.get('color')
    
    #UserNoがない場合はエラー
    if(userNo is 'None'):
        return HttpResponse('UserNo None')
    #画像のクエリ作成
    ac = models.QuerySet(Photo)
    #画像からUserNoで抽出
    ac =  ac.filter(userNo = userNo)
    #カテゴリで選別
    if(cate is not None):
        ac = ac.filter(cate = cate)
    if(sub is not None):
        ac = ac.filter(sub = cate)
    if(color is not None):
        ac = ac.filter(color = cate)
    
    #クエリをリスト型にする 画像のあるURLを送る
    path_list  = list(ac.values_list('FilePath',flat=True))
    cate_list  = list(ac.values_list('cate',flat=True))
    sub_list   = list(ac.values_list('sub',flat=True))
    color_list = list(ac.values_list('color',flat=True))
    dress_value_list = list(ac.values_list('dress_value',flat=True))
    casual_value_list = list(ac.values_list('casual_value',flat=True))
    simple_value_list = list(ac.values_list('simple_value',flat=True))
    tag1 = list(ac.values_list('tag',flat=True))
    tag2 = list(ac.values_list('tag2',flat=True))
    tag3 = list(ac.values_list('tag3',flat=True))
    tag4 = list(ac.values_list('tag4',flat=True))
    
    dress = sum(dress_value_list)
    casual = sum(casual_value_list)
    simple = sum(simple_value_list)
    
    
    

    print(path_list)
    #dict型にする
    d = {
        'path_list' :path_list,
        'cate_list' :cate_list,
        'sub_list'  :sub_list,
        'color_list':color_list,
        'dress':dress,
        'casual':casual,
        'simple':simple,
        'dress_value_list':dress_value_list,
        'casual_value_list':casual_value_list,
        'simple_value_list':simple_value_list,
        'tag1':tag1,
        'tag2':tag2,
        'tag3':tag3,
        'tag4':tag4
    }
    return JsonResponse(d)

@csrf_exempt
def changeAccount(request):
    if request.method == 'GET':
        return HttpResponse("")
    userNo = request.POST['UserNo']
    name   = request.POST['name']
    jiko   = request.POST['jiko']
    mytype   = request.POST['type']
    age    = request.POST['age']

    myAccount = models.QuerySet(Account).filter(id=userNo).first()
    myAccount.name = name
    myAccount.jiko = jiko
    myAccount.type = mytype
    myAccount.age  = age
    myAccount.save()

    return HttpResponse('account change complete')
def getAccount(request):
    userNo = request.GET.get('userNo')
    myAccount = models.QuerySet(Account).filter(id=userNo)
    age = list(myAccount.values_list('age',flat=True))[0]
    name = list(myAccount.values_list('name',flat=True))[0]
    jiko = list(myAccount.values_list('jiko',flat=True))[0]
    sex = list(myAccount.values_list('sex',flat=True))[0]
    type = list(myAccount.values_list('type',flat=True))[0]

    return HttpResponse(str(age)+','+name+','+jiko+','+sex+','+type)
    
def getCodenate(request):
    import numpy as np

    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))
    #---------ハイパーパラメータ---------
    type_DCS_weight = 1
    type_match_tag_weight = 10
    type_match_vol_weight = 10

    good_tag1_weight = 1.5
    good_tag2_weight = 1
    good_tag3_weight = 0.5
    good_tag4_weight = 0.25
    bad_tag1_weight = 1.5
    bad_tag2_weight = 1
    bad_tag3_weight = 0.5
    bad_tag4_weight = 0.25   
    #-----------------------------------

    photo_all = models.QuerySet(Photo)
    #ユーザーの服を全部出力
    user_photo_all  = photo_all.filter(userNo=userNo)
    #カテゴリ別のクエリを抽出
    user_tops_all = user_photo_all.filter(cate='tops')
    user_botoms_all = user_photo_all.filter(cate='botoms')
    user_shoese_all = user_photo_all.filter(cate='shoese')

    tops_count = user_photo_all.filter(cate='tops').count()
    botoms_count = user_photo_all.filter(cate='botoms').count()
    shoese_count = user_photo_all.filter(cate='shoese').count()

    #アウターは冬用　まだ未開発
    outer_count = user_photo_all.filter(cate='outer').count()
    
    #服の数でコーディネートできるか判定
    if tops_count < 1:
        return HttpResponse('tops no item')
    if botoms_count < 1:
        return HttpResponse('botoms no item')
    if shoese_count < 1:
        return HttpResponse('shoese no item')


    user_type = list(models.QuerySet(Account).filter(id=userNo).values_list('type',flat=True))[0]
    #------------自分の好きなタイプのドレス率　カジュアル率　シンプル率の差が一番少ない順にする--------------
    type_temp_all = models.QuerySet(Codnate_type_temp)
    user_like_type_temp = type_temp_all.filter(code_type=user_type)
    bad_codnate_list = models.QuerySet(Bad_Codnate)

    type_dress_value = list(user_like_type_temp.values_list('dress_value',flat=True))[0]
    type_casual_value = list(user_like_type_temp.values_list('casual_value',flat=True))[0]
    type_simple_value = list(user_like_type_temp.values_list('simple_value',flat=True))[0]


    tops_dress_value_list = list(user_tops_all.values_list('dress_value',flat=True))
    tops_casual_value_list = list(user_tops_all.values_list('casual_value',flat=True))
    tops_simple_value_list = list(user_tops_all.values_list('simple_value',flat=True))

    botoms_dress_value_list = list(user_botoms_all.values_list('dress_value',flat=True))
    botoms_casual_value_list = list(user_botoms_all.values_list('casual_value',flat=True))
    botoms_simple_value_list = list(user_botoms_all.values_list('simple_value',flat=True))

    shoese_dress_value_list = list(user_shoese_all.values_list('dress_value',flat=True))
    shoese_casual_value_list = list(user_shoese_all.values_list('casual_value',flat=True))
    shoese_simple_value_list = list(user_shoese_all.values_list('simple_value',flat=True))


    type_filter_list = []
    type_filter_idx_list = []

    for tops_idx in range(tops_count):
        for botoms_idx in range(botoms_count):
            for shoese_idx in range(shoese_count):
                
                
                
                dress_sum = tops_dress_value_list[tops_idx] + botoms_dress_value_list[botoms_idx] + shoese_dress_value_list[shoese_idx]
                casual_sum = tops_casual_value_list[tops_idx] + botoms_casual_value_list[botoms_idx] + shoese_casual_value_list[shoese_idx]
                simple_sum = tops_simple_value_list[tops_idx] + botoms_simple_value_list[botoms_idx] + shoese_simple_value_list[shoese_idx]
                dress_per = dress_sum / (dress_sum + casual_sum + simple_sum)
                casual_per = casual_sum / (dress_sum + casual_sum + simple_sum)
                simple_per = simple_sum / (dress_sum + casual_sum + simple_sum)

                type_absolute =  abs(type_dress_value - dress_per) + abs(type_casual_value - casual_per) + abs(type_simple_value - simple_per)

                type_filter_list.append(type_absolute)
                type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])

    #------------タグに一番当てはまっている組み合わせを評価-------------
    tag1 = list(user_like_type_temp.values_list('tag1',flat=True))[0]
    tag2 = list(user_like_type_temp.values_list('tag2',flat=True))[0]
    tag3 = list(user_like_type_temp.values_list('tag3',flat=True))[0]
    tag4 = list(user_like_type_temp.values_list('tag4',flat=True))[0]
    if 10 < len(type_filter_list):
        n = int(len(type_filter_list)/2)
        sorted_idx = np.argsort(type_filter_list)
    else:
        n = len(type_filter_list)
        sorted_idx = np.argsort(type_filter_list)
    tag_sum_list = []
    tag_idx_list = []

    print(sorted_idx)
    
    user_photo_tops_tag1 = list(user_tops_all.values_list('tag',flat=True))
    user_photo_tops_tag2 = list(user_tops_all.values_list('tag2',flat=True))
    user_photo_tops_tag3 = list(user_tops_all.values_list('tag3',flat=True))
    user_photo_tops_tag4 = list(user_tops_all.values_list('tag4',flat=True))

    user_photo_botoms_tag1 = list(user_botoms_all.values_list('tag',flat=True))
    user_photo_botoms_tag2 = list(user_botoms_all.values_list('tag2',flat=True))
    user_photo_botoms_tag3 = list(user_botoms_all.values_list('tag3',flat=True))
    user_photo_botoms_tag4 = list(user_botoms_all.values_list('tag4',flat=True))

    user_photo_shoese_tag1 = list(user_shoese_all.values_list('tag',flat=True))
    user_photo_shoese_tag2 = list(user_shoese_all.values_list('tag2',flat=True))
    user_photo_shoese_tag3 = list(user_shoese_all.values_list('tag3',flat=True))
    user_photo_shoese_tag4 = list(user_shoese_all.values_list('tag4',flat=True))

    user_good_codnate = models.QuerySet(Good_Codnate).filter(userNo=userNo)

    user_like_tops_tag1_list = list(user_good_codnate.values_list('tops_tag1',flat=True))
    user_like_tops_tag2_list = list(user_good_codnate.values_list('tops_tag2',flat=True))
    user_like_tops_tag3_list = list(user_good_codnate.values_list('tops_tag3',flat=True))
    user_like_tops_tag4_list = list(user_good_codnate.values_list('tops_tag4',flat=True))

    user_like_botoms_tag1_list = list(user_good_codnate.values_list('botoms_tag1',flat=True))
    user_like_botoms_tag2_list = list(user_good_codnate.values_list('botoms_tag2',flat=True))
    user_like_botoms_tag3_list = list(user_good_codnate.values_list('botoms_tag3',flat=True))
    user_like_botoms_tag4_list = list(user_good_codnate.values_list('botoms_tag4',flat=True))

    user_like_shoese_tag1_list = list(user_good_codnate.values_list('shoese_tag1',flat=True))
    user_like_shoese_tag2_list = list(user_good_codnate.values_list('shoese_tag2',flat=True))
    user_like_shoese_tag3_list = list(user_good_codnate.values_list('shoese_tag3',flat=True))
    user_like_shoese_tag4_list = list(user_good_codnate.values_list('shoese_tag4',flat=True))

    user_bad_codnate = models.QuerySet(Bad_Codnate).filter(userNo=userNo)

    user_bad_tops_tag1_list = list(user_bad_codnate.values_list('tops_tag1',flat=True))
    user_bad_tops_tag2_list = list(user_bad_codnate.values_list('tops_tag2',flat=True))
    user_bad_tops_tag3_list = list(user_bad_codnate.values_list('tops_tag3',flat=True))
    user_bad_tops_tag4_list = list(user_bad_codnate.values_list('tops_tag4',flat=True))

    user_bad_botoms_tag1_list = list(user_bad_codnate.values_list('botoms_tag1',flat=True))
    user_bad_botoms_tag2_list = list(user_bad_codnate.values_list('botoms_tag2',flat=True))
    user_bad_botoms_tag3_list = list(user_bad_codnate.values_list('botoms_tag3',flat=True))
    user_bad_botoms_tag4_list = list(user_bad_codnate.values_list('botoms_tag4',flat=True))

    user_bad_shoese_tag1_list = list(user_bad_codnate.values_list('shoese_tag1',flat=True))
    user_bad_shoese_tag2_list = list(user_bad_codnate.values_list('shoese_tag2',flat=True))
    user_bad_shoese_tag3_list = list(user_bad_codnate.values_list('shoese_tag3',flat=True))
    user_bad_shoese_tag4_list = list(user_bad_codnate.values_list('shoese_tag4',flat=True))
    



    for code_idx in range(n):
        tag_list = []
        user_like_tag_point = 0
        user_bad_tag_point = 0
        tag_list.append(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])
        
        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        tag_list.append(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])
        
        tag_list.append(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        tag1_count = tag_list.count(tag1) 
        tag2_count = tag_list.count(tag2) 
        tag3_count = tag_list.count(tag3) 
        tag4_count = tag_list.count(tag4) 



        tag_sum_list.append(tag1_count*type_match_tag_weight + tag2_count*type_match_tag_weight + tag3_count*type_match_tag_weight + tag4_count*type_match_tag_weight - type_filter_list[sorted_idx[code_idx]]*type_DCS_weight + user_like_tag_point - user_bad_tag_point)
        tag_idx_list.append(type_filter_idx_list[sorted_idx[code_idx]])
    #----------控え目か派手かで評価---------

    vol = list(user_like_type_temp.values_list('vol',flat=True))[0]

    user_photo_tops_vol_list = list(user_tops_all.values_list('vol',flat=True))
    user_photo_botoms_vol_list = list(user_botoms_all.values_list('vol',flat=True))
    user_photo_shoese_vol_list = list(user_shoese_all.values_list('vol',flat=True))
    for i in range(len(tag_sum_list)):
        vol_list = []
        vol_list.append(user_photo_tops_vol_list[tag_idx_list[i][0]])
        vol_list.append(user_photo_botoms_vol_list[tag_idx_list[i][1]])
        vol_list.append(user_photo_shoese_vol_list[tag_idx_list[i][2]])
        vol_count = vol_list.count(vol)
        tag_sum_list[i] = tag_sum_list[i] + vol_count * type_match_vol_weight
    

    tag_sorted_idx = np.argsort(tag_sum_list)[::-1]
    if 6 <= len(tag_sorted_idx):
        res_idx_list = tag_sorted_idx[0:6]
    else:
        res_idx_list = tag_sorted_idx
    #-------------一番評価の高い服を出力------------
    res_tops_path =[]
    res_botoms_path = []
    res_shoese_path = []

    res_tops_color = []
    res_botoms_color = []
    res_shoese_color = []

    res_tops_sub = []
    res_botoms_sub = []
    res_shoese_sub = []

    sample_list = []

    tops_path_list = list(user_tops_all.values_list('FilePath',flat=True))
    botoms_path_list = list(user_botoms_all.values_list('FilePath',flat=True))
    shoese_path_list = list(user_shoese_all.values_list('FilePath',flat=True))

    tops_color_list = list(user_tops_all.values_list('color',flat=True))
    botoms_color_list = list(user_botoms_all.values_list('color',flat=True))
    shoese_color_list = list(user_shoese_all.values_list('color',flat=True))

    tops_sub_list = list(user_tops_all.values_list('sub',flat=True))
    botoms_sub_list = list(user_botoms_all.values_list('sub',flat=True))
    shoese_sub_list = list(user_shoese_all.values_list('sub',flat=True))

    codnate_sample = models.QuerySet(Codnate_sample)


    for i in range(len(res_idx_list)):
        res_tops_path.append(tops_path_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_color.append(tops_color_list[tag_idx_list[res_idx_list[i]][0]])
        tops_sub = tops_sub_list[tag_idx_list[res_idx_list[i]][0]]
        res_tops_sub.append(tops_sub)
            
        res_botoms_path.append(botoms_path_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_color.append(botoms_color_list[tag_idx_list[res_idx_list[i]][1]])
        botoms_sub = botoms_sub_list[tag_idx_list[res_idx_list[i]][1]]
        res_botoms_sub.append(botoms_sub)
               
        res_shoese_path.append(shoese_path_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_color.append(shoese_color_list[tag_idx_list[res_idx_list[i]][2]])
        shoese_sub = shoese_sub_list[tag_idx_list[res_idx_list[i]][2]]
        res_shoese_sub.append(shoese_sub)
        sample = list(codnate_sample.filter(sub1=tops_sub,sub2=botoms_sub,sub3=shoese_sub).values_list('sample',flat=True))
        if len(sample) > 0:
            sample_list.append(sample[0])
        else:
            sample_list.append("")

        
    

    d = {
        'tops_path':res_tops_path,
        'tops_color':res_tops_color,
        'tops_sub':res_tops_sub,
        'botoms_path':res_botoms_path,
        'botoms_color':res_botoms_color,
        'botoms_sub':res_botoms_sub,
        'shoese_path':res_shoese_path,
        'shoese_color':res_shoese_color,
        'shoese_sub':res_shoese_sub,
        'codnate_sample':sample_list
    }
    print(d)
    return JsonResponse(d)
    
@csrf_exempt    
def bad_codnate_post(request):
    if request.method == 'GET':
        return HttpResponse()
    try:
        userNo = request.POST['user_no']

        tops_path = request.POST['tops_path']
        botoms_path = request.POST['botoms_path']
        shoese_path = request.POST['shoese_path']

        user_photo_all = models.QuerySet(Photo).filter(userNo=userNo)

        tops_tag1 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag',flat=True))[0]
        tops_tag2 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag2',flat=True))[0]
        tops_tag3 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag3',flat=True))[0]
        tops_tag4 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag4',flat=True))[0]
    
        botoms_tag1 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag',flat=True))[0]
        botoms_tag2 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag2',flat=True))[0]
        botoms_tag3 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag3',flat=True))[0]
        botoms_tag4 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag4',flat=True))[0]

        shoese_tag1 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag',flat=True))[0]
        shoese_tag2 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag2',flat=True))[0]
        shoese_tag3 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag3',flat=True))[0]
        shoese_tag4 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag4',flat=True))[0]
        
        bad = Bad_Codnate(userNo=userNo,tops_tag1=tops_tag1,tops_tag2=tops_tag2,tops_tag3=tops_tag3,tops_tag4=tops_tag4,
                                        botoms_tag1=botoms_tag1,botoms_tag2=botoms_tag2,botoms_tag3=botoms_tag3,botoms_tag4=botoms_tag4,
                                        shoese_tag1=shoese_tag1,shoese_tag2=shoese_tag2,shoese_tag3=shoese_tag3,shoese_tag4=shoese_tag4)
        bad.save()

        return HttpResponse('bad complete')
    except Exception:
        return HttpResponse('totyuude error')


@csrf_exempt    
def good_codnate_post(request):
    if request.method == 'GET':
        return HttpResponse()
    try:
        userNo = request.POST['user_no']

        tops_path = request.POST['tops_path']
        botoms_path = request.POST['botoms_path']
        shoese_path = request.POST['shoese_path']

        user_photo_all = models.QuerySet(Photo).filter(userNo=userNo)
        tops = user_photo_all.filter(FilePath=tops_path)
        
        tops_tag1 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag',flat=True))[0]
        tops_tag2 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag2',flat=True))[0]
        tops_tag3 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag3',flat=True))[0]
        tops_tag4 = list(user_photo_all.filter(FilePath=tops_path).values_list('tag4',flat=True))[0]

        

        botoms_tag1 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag',flat=True))[0]
        botoms_tag2 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag2',flat=True))[0]
        botoms_tag3 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag3',flat=True))[0]
        botoms_tag4 = list(user_photo_all.filter(FilePath=botoms_path).values_list('tag4',flat=True))[0]

        shoese_tag1 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag',flat=True))[0]
        shoese_tag2 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag2',flat=True))[0]
        shoese_tag3 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag3',flat=True))[0]
        shoese_tag4 = list(user_photo_all.filter(FilePath=shoese_path).values_list('tag4',flat=True))[0]
        
        good = Good_Codnate(userNo=userNo,tops_tag1=tops_tag1,tops_tag2=tops_tag2,tops_tag3=tops_tag3,tops_tag4=tops_tag4,
                                        botoms_tag1=botoms_tag1,botoms_tag2=botoms_tag2,botoms_tag3=botoms_tag3,botoms_tag4=botoms_tag4,
                                        shoese_tag1=shoese_tag1,shoese_tag2=shoese_tag2,shoese_tag3=shoese_tag3,shoese_tag4=shoese_tag4)

        good.save()

        return HttpResponse('good complete')
    except Exception:
        return HttpResponse('totyuude error')

def get_recomend_web_item_tops(request):
    import numpy as np

    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))

    recomend_all = models.QuerySet(Recomend_item)
    #---------ハイパーパラメータ---------
    type_DCS_weight = 1
    type_match_tag_weight = 10
    type_match_vol_weight = 10

    good_tag1_weight = 1.5
    good_tag2_weight = 1
    good_tag3_weight = 0.5
    good_tag4_weight = 0.25
    bad_tag1_weight = 1.5
    bad_tag2_weight = 1
    bad_tag3_weight = 0.5
    bad_tag4_weight = 0.25   
    #-----------------------------------
    #ユーザーの服を全部出力
    user_photo_all  = photo_all.filter(userNo=userNo)
    #カテゴリ別のクエリを抽出
    user_tops_all = recomend_all.filter(cate='トップス')
    user_botoms_all = user_photo_all.filter(cate='botoms')
    user_shoese_all = user_photo_all.filter(cate='shoese')

    tops_count = user_photo_all.filter(cate='tops').count()
    botoms_count = user_photo_all.filter(cate='botoms').count()
    shoese_count = user_photo_all.filter(cate='shoese').count()

    #アウターは冬用　まだ未開発
    outer_count = user_photo_all.filter(cate='outer').count()
    
    #服の数でコーディネートできるか判定
    if botoms_count < 1:
        return HttpResponse('botoms no item')
    if shoese_count < 1:
        return HttpResponse('shoese no item')


    user_type = list(models.QuerySet(Account).filter(id=userNo).values_list('type',flat=True))[0]
    print(user_type)
    #------------自分の好きなタイプのドレス率　カジュアル率　シンプル率の差が一番少ない順にする--------------
    type_temp_all = models.QuerySet(Codnate_type_temp)
    user_like_type_temp = type_temp_all.filter(code_type=user_type)
    bad_codnate_list = models.QuerySet(Bad_Codnate)

    type_dress_value = list(user_like_type_temp.values_list('dress_value',flat=True))[0]
    type_casual_value = list(user_like_type_temp.values_list('casual_value',flat=True))[0]
    type_simple_value = list(user_like_type_temp.values_list('simple_value',flat=True))[0]

    tops_dress_value_list = list(user_tops_all.values_list('dress_value',flat=True))
    tops_casual_value_list = list(user_tops_all.values_list('casual_value',flat=True))
    tops_simple_value_list = list(user_tops_all.values_list('simple_value',flat=True))

    botoms_dress_value_list = list(user_botoms_all.values_list('dress_value',flat=True))
    botoms_casual_value_list = list(user_botoms_all.values_list('casual_value',flat=True))
    botoms_simple_value_list = list(user_botoms_all.values_list('simple_value',flat=True))

    shoese_dress_value_list = list(user_shoese_all.values_list('dress_value',flat=True))
    shoese_casual_value_list = list(user_shoese_all.values_list('casual_value',flat=True))
    shoese_simple_value_list = list(user_shoese_all.values_list('simple_value',flat=True))


    type_filter_list = []
    type_filter_idx_list = []

    for tops_idx in range(tops_count):
        for botoms_idx in range(botoms_count):
            for shoese_idx in range(shoese_count):
                                
                dress_sum = tops_dress_value_list[tops_idx] + botoms_dress_value_list[botoms_idx] + shoese_dress_value_list[shoese_idx]
                casual_sum = tops_casual_value_list[tops_idx] + botoms_casual_value_list[botoms_idx] + shoese_casual_value_list[shoese_idx]
                simple_sum = tops_simple_value_list[tops_idx] + botoms_simple_value_list[botoms_idx] + shoese_simple_value_list[shoese_idx]
                dress_per = dress_sum / (dress_sum + casual_sum + simple_sum)
                casual_per = casual_sum / (dress_sum + casual_sum + simple_sum)
                simple_per = simple_sum / (dress_sum + casual_sum + simple_sum)

                type_absolute =  abs(type_dress_value - dress_per) + abs(type_casual_value - casual_per) + abs(type_simple_value - simple_per)

                type_filter_list.append(type_absolute)
                type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])

    #------------タグに一番当てはまっている組み合わせを評価-------------
    tag1 = list(user_like_type_temp.values_list('tag1',flat=True))[0]
    tag2 = list(user_like_type_temp.values_list('tag2',flat=True))[0]
    tag3 = list(user_like_type_temp.values_list('tag3',flat=True))[0]
    tag4 = list(user_like_type_temp.values_list('tag4',flat=True))[0]
    if 10 < len(type_filter_list):
        n = int(len(type_filter_list)/2)
        sorted_idx = np.argsort(type_filter_list)
    else:
        n = len(type_filter_list)
        sorted_idx = np.argsort(type_filter_list)
    tag_sum_list = []
    tag_idx_list = []

    
    user_photo_tops_tag1 = list(user_tops_all.values_list('tag',flat=True))
    user_photo_tops_tag2 = list(user_tops_all.values_list('tag2',flat=True))
    user_photo_tops_tag3 = list(user_tops_all.values_list('tag3',flat=True))
    user_photo_tops_tag4 = list(user_tops_all.values_list('tag4',flat=True))

    user_photo_botoms_tag1 = list(user_botoms_all.values_list('tag',flat=True))
    user_photo_botoms_tag2 = list(user_botoms_all.values_list('tag2',flat=True))
    user_photo_botoms_tag3 = list(user_botoms_all.values_list('tag3',flat=True))
    user_photo_botoms_tag4 = list(user_botoms_all.values_list('tag4',flat=True))

    user_photo_shoese_tag1 = list(user_shoese_all.values_list('tag',flat=True))
    user_photo_shoese_tag2 = list(user_shoese_all.values_list('tag2',flat=True))
    user_photo_shoese_tag3 = list(user_shoese_all.values_list('tag3',flat=True))
    user_photo_shoese_tag4 = list(user_shoese_all.values_list('tag4',flat=True))

    user_good_codnate = models.QuerySet(Good_Codnate).filter(userNo=userNo)

    user_like_tops_tag1_list = list(user_good_codnate.values_list('tops_tag1',flat=True))
    user_like_tops_tag2_list = list(user_good_codnate.values_list('tops_tag2',flat=True))
    user_like_tops_tag3_list = list(user_good_codnate.values_list('tops_tag3',flat=True))
    user_like_tops_tag4_list = list(user_good_codnate.values_list('tops_tag4',flat=True))

    user_like_botoms_tag1_list = list(user_good_codnate.values_list('botoms_tag1',flat=True))
    user_like_botoms_tag2_list = list(user_good_codnate.values_list('botoms_tag2',flat=True))
    user_like_botoms_tag3_list = list(user_good_codnate.values_list('botoms_tag3',flat=True))
    user_like_botoms_tag4_list = list(user_good_codnate.values_list('botoms_tag4',flat=True))

    user_like_shoese_tag1_list = list(user_good_codnate.values_list('shoese_tag1',flat=True))
    user_like_shoese_tag2_list = list(user_good_codnate.values_list('shoese_tag2',flat=True))
    user_like_shoese_tag3_list = list(user_good_codnate.values_list('shoese_tag3',flat=True))
    user_like_shoese_tag4_list = list(user_good_codnate.values_list('shoese_tag4',flat=True))

    user_bad_codnate = models.QuerySet(Bad_Codnate).filter(userNo=userNo)

    user_bad_tops_tag1_list = list(user_bad_codnate.values_list('tops_tag1',flat=True))
    user_bad_tops_tag2_list = list(user_bad_codnate.values_list('tops_tag2',flat=True))
    user_bad_tops_tag3_list = list(user_bad_codnate.values_list('tops_tag3',flat=True))
    user_bad_tops_tag4_list = list(user_bad_codnate.values_list('tops_tag4',flat=True))

    user_bad_botoms_tag1_list = list(user_bad_codnate.values_list('botoms_tag1',flat=True))
    user_bad_botoms_tag2_list = list(user_bad_codnate.values_list('botoms_tag2',flat=True))
    user_bad_botoms_tag3_list = list(user_bad_codnate.values_list('botoms_tag3',flat=True))
    user_bad_botoms_tag4_list = list(user_bad_codnate.values_list('botoms_tag4',flat=True))

    user_bad_shoese_tag1_list = list(user_bad_codnate.values_list('shoese_tag1',flat=True))
    user_bad_shoese_tag2_list = list(user_bad_codnate.values_list('shoese_tag2',flat=True))
    user_bad_shoese_tag3_list = list(user_bad_codnate.values_list('shoese_tag3',flat=True))
    user_bad_shoese_tag4_list = list(user_bad_codnate.values_list('shoese_tag4',flat=True))
    



    for code_idx in range(n):
        tag_list = []
        user_like_tag_point = 0
        user_bad_tag_point = 0
        tag_list.append(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])
        
        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        tag_list.append(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])
        
        tag_list.append(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        tag1_count = tag_list.count(tag1) 
        tag2_count = tag_list.count(tag2) 
        tag3_count = tag_list.count(tag3) 
        tag4_count = tag_list.count(tag4) 



        tag_sum_list.append(tag1_count*type_match_tag_weight + tag2_count*type_match_tag_weight + tag3_count*type_match_tag_weight + tag4_count*type_match_tag_weight - type_filter_list[sorted_idx[code_idx]]*type_DCS_weight + user_like_tag_point - user_bad_tag_point)
        tag_idx_list.append(type_filter_idx_list[sorted_idx[code_idx]])
    #----------控え目か派手かで評価---------

    vol = list(user_like_type_temp.values_list('vol',flat=True))[0]

    user_photo_tops_vol_list = list(user_tops_all.values_list('vol',flat=True))
    user_photo_botoms_vol_list = list(user_botoms_all.values_list('vol',flat=True))
    user_photo_shoese_vol_list = list(user_shoese_all.values_list('vol',flat=True))
    for i in range(len(tag_sum_list)):
        vol_list = []
        vol_list.append(user_photo_tops_vol_list[tag_idx_list[i][0]])
        vol_list.append(user_photo_botoms_vol_list[tag_idx_list[i][1]])
        vol_list.append(user_photo_shoese_vol_list[tag_idx_list[i][2]])
        vol_count = vol_list.count(vol)
        tag_sum_list[i] = tag_sum_list[i] + vol_count * type_match_vol_weight
    

    tag_sorted_idx = np.argsort(tag_sum_list)[::-1]
    if 3 <= len(tag_sorted_idx):
        res_idx_list = tag_sorted_idx[0:1]
    else:
        res_idx_list = tag_sorted_idx
    print(res_idx_list)
    #-------------一番評価の高い服を出力------------
    res_tops_path =[]
    res_botoms_path = []
    res_shoese_path = []

    res_tops_color = []
    res_botoms_color = []
    res_shoese_color = []

    res_tops_sub = []
    res_botoms_sub = []
    res_shoese_sub = []


    tops_path_list = list(user_tops_all.values_list('FilePath',flat=True))
    botoms_path_list = list(user_botoms_all.values_list('FilePath',flat=True))
    shoese_path_list = list(user_shoese_all.values_list('FilePath',flat=True))

    tops_color_list = list(user_tops_all.values_list('color',flat=True))
    botoms_color_list = list(user_botoms_all.values_list('color',flat=True))
    shoese_color_list = list(user_shoese_all.values_list('color',flat=True))

    tops_sub_list = list(user_tops_all.values_list('sub',flat=True))
    botoms_sub_list = list(user_botoms_all.values_list('sub',flat=True))
    shoese_sub_list = list(user_shoese_all.values_list('sub',flat=True))

    for i in range(len(res_idx_list)):
        res_tops_path.append(tops_path_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_color.append(tops_color_list[tag_idx_list[res_idx_list[i]][0]])
        tops_sub = tops_sub_list[tag_idx_list[res_idx_list[i]][0]]
        res_tops_sub.append(tops_sub)
            
        res_botoms_path.append(botoms_path_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_color.append(botoms_color_list[tag_idx_list[res_idx_list[i]][1]])
        botoms_sub = botoms_sub_list[tag_idx_list[res_idx_list[i]][1]]
        res_botoms_sub.append(botoms_sub)
               
        res_shoese_path.append(shoese_path_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_color.append(shoese_color_list[tag_idx_list[res_idx_list[i]][2]])
        shoese_sub = shoese_sub_list[tag_idx_list[res_idx_list[i]][2]]
        res_shoese_sub.append(shoese_sub)


    d = {
        'tops_path':res_tops_path,
        'tops_color':res_tops_color,
        'tops_sub':res_tops_sub,
        'botoms_path':res_botoms_path,
        'botoms_color':res_botoms_color,
        'botoms_sub':res_botoms_sub,
        'shoese_path':res_shoese_path,
        'shoese_color':res_shoese_color,
        'shoese_sub':res_shoese_sub,
    }
    print(d)
    return JsonResponse(d)

def get_recomend_web_item_botoms(request):
    import numpy as np

    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))

    recomend_all = models.QuerySet(Recomend_item)
    #---------ハイパーパラメータ---------
    type_DCS_weight = 1
    type_match_tag_weight = 10
    type_match_vol_weight = 10

    good_tag1_weight = 1.5
    good_tag2_weight = 1
    good_tag3_weight = 0.5
    good_tag4_weight = 0.25
    bad_tag1_weight = 1.5
    bad_tag2_weight = 1
    bad_tag3_weight = 0.5
    bad_tag4_weight = 0.25   
    #-----------------------------------
    #ユーザーの服を全部出力
    user_photo_all  = photo_all.filter(userNo=userNo)
    #カテゴリ別のクエリを抽出
    user_tops_all = user_photo_all.filter(cate='tops')
    user_botoms_all = recomend_all.filter(Q(cate='パンツ')|Q(cate='スカート')).distinct()
    user_shoese_all = user_photo_all.filter(cate='shoese')

    tops_count = user_photo_all.filter(cate='tops').count()
    botoms_count = user_photo_all.filter(cate='botoms').count()
    shoese_count = user_photo_all.filter(cate='shoese').count()

    #アウターは冬用　まだ未開発
    outer_count = user_photo_all.filter(cate='outer').count()
    
    #服の数でコーディネートできるか判定
    if tops_count < 1:
        return HttpResponse('tops no item')
    if shoese_count < 1:
        return HttpResponse('shoese no item')


    user_type = list(models.QuerySet(Account).filter(id=userNo).values_list('type',flat=True))[0]
    print(user_type)
    #------------自分の好きなタイプのドレス率　カジュアル率　シンプル率の差が一番少ない順にする--------------
    type_temp_all = models.QuerySet(Codnate_type_temp)
    user_like_type_temp = type_temp_all.filter(code_type=user_type)
    bad_codnate_list = models.QuerySet(Bad_Codnate)

    type_dress_value = list(user_like_type_temp.values_list('dress_value',flat=True))[0]
    type_casual_value = list(user_like_type_temp.values_list('casual_value',flat=True))[0]
    type_simple_value = list(user_like_type_temp.values_list('simple_value',flat=True))[0]

    tops_dress_value_list = list(user_tops_all.values_list('dress_value',flat=True))
    tops_casual_value_list = list(user_tops_all.values_list('casual_value',flat=True))
    tops_simple_value_list = list(user_tops_all.values_list('simple_value',flat=True))

    botoms_dress_value_list = list(user_botoms_all.values_list('dress_value',flat=True))
    botoms_casual_value_list = list(user_botoms_all.values_list('casual_value',flat=True))
    botoms_simple_value_list = list(user_botoms_all.values_list('simple_value',flat=True))

    shoese_dress_value_list = list(user_shoese_all.values_list('dress_value',flat=True))
    shoese_casual_value_list = list(user_shoese_all.values_list('casual_value',flat=True))
    shoese_simple_value_list = list(user_shoese_all.values_list('simple_value',flat=True))


    type_filter_list = []
    type_filter_idx_list = []

    for tops_idx in range(tops_count):
        for botoms_idx in range(botoms_count):
            for shoese_idx in range(shoese_count):
                                
                dress_sum = tops_dress_value_list[tops_idx] + botoms_dress_value_list[botoms_idx] + shoese_dress_value_list[shoese_idx]
                casual_sum = tops_casual_value_list[tops_idx] + botoms_casual_value_list[botoms_idx] + shoese_casual_value_list[shoese_idx]
                simple_sum = tops_simple_value_list[tops_idx] + botoms_simple_value_list[botoms_idx] + shoese_simple_value_list[shoese_idx]
                dress_per = dress_sum / (dress_sum + casual_sum + simple_sum)
                casual_per = casual_sum / (dress_sum + casual_sum + simple_sum)
                simple_per = simple_sum / (dress_sum + casual_sum + simple_sum)

                type_absolute =  abs(type_dress_value - dress_per) + abs(type_casual_value - casual_per) + abs(type_simple_value - simple_per)

                type_filter_list.append(type_absolute)
                type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])

    #------------タグに一番当てはまっている組み合わせを評価-------------
    tag1 = list(user_like_type_temp.values_list('tag1',flat=True))[0]
    tag2 = list(user_like_type_temp.values_list('tag2',flat=True))[0]
    tag3 = list(user_like_type_temp.values_list('tag3',flat=True))[0]
    tag4 = list(user_like_type_temp.values_list('tag4',flat=True))[0]
    if 10 < len(type_filter_list):
        n = int(len(type_filter_list)/2)
        sorted_idx = np.argsort(type_filter_list)
    else:
        n = len(type_filter_list)
        sorted_idx = np.argsort(type_filter_list)
    tag_sum_list = []
    tag_idx_list = []

    
    user_photo_tops_tag1 = list(user_tops_all.values_list('tag',flat=True))
    user_photo_tops_tag2 = list(user_tops_all.values_list('tag2',flat=True))
    user_photo_tops_tag3 = list(user_tops_all.values_list('tag3',flat=True))
    user_photo_tops_tag4 = list(user_tops_all.values_list('tag4',flat=True))

    user_photo_botoms_tag1 = list(user_botoms_all.values_list('tag',flat=True))
    user_photo_botoms_tag2 = list(user_botoms_all.values_list('tag2',flat=True))
    user_photo_botoms_tag3 = list(user_botoms_all.values_list('tag3',flat=True))
    user_photo_botoms_tag4 = list(user_botoms_all.values_list('tag4',flat=True))

    user_photo_shoese_tag1 = list(user_shoese_all.values_list('tag',flat=True))
    user_photo_shoese_tag2 = list(user_shoese_all.values_list('tag2',flat=True))
    user_photo_shoese_tag3 = list(user_shoese_all.values_list('tag3',flat=True))
    user_photo_shoese_tag4 = list(user_shoese_all.values_list('tag4',flat=True))

    user_good_codnate = models.QuerySet(Good_Codnate).filter(userNo=userNo)

    user_like_tops_tag1_list = list(user_good_codnate.values_list('tops_tag1',flat=True))
    user_like_tops_tag2_list = list(user_good_codnate.values_list('tops_tag2',flat=True))
    user_like_tops_tag3_list = list(user_good_codnate.values_list('tops_tag3',flat=True))
    user_like_tops_tag4_list = list(user_good_codnate.values_list('tops_tag4',flat=True))

    user_like_botoms_tag1_list = list(user_good_codnate.values_list('botoms_tag1',flat=True))
    user_like_botoms_tag2_list = list(user_good_codnate.values_list('botoms_tag2',flat=True))
    user_like_botoms_tag3_list = list(user_good_codnate.values_list('botoms_tag3',flat=True))
    user_like_botoms_tag4_list = list(user_good_codnate.values_list('botoms_tag4',flat=True))

    user_like_shoese_tag1_list = list(user_good_codnate.values_list('shoese_tag1',flat=True))
    user_like_shoese_tag2_list = list(user_good_codnate.values_list('shoese_tag2',flat=True))
    user_like_shoese_tag3_list = list(user_good_codnate.values_list('shoese_tag3',flat=True))
    user_like_shoese_tag4_list = list(user_good_codnate.values_list('shoese_tag4',flat=True))

    user_bad_codnate = models.QuerySet(Bad_Codnate).filter(userNo=userNo)

    user_bad_tops_tag1_list = list(user_bad_codnate.values_list('tops_tag1',flat=True))
    user_bad_tops_tag2_list = list(user_bad_codnate.values_list('tops_tag2',flat=True))
    user_bad_tops_tag3_list = list(user_bad_codnate.values_list('tops_tag3',flat=True))
    user_bad_tops_tag4_list = list(user_bad_codnate.values_list('tops_tag4',flat=True))

    user_bad_botoms_tag1_list = list(user_bad_codnate.values_list('botoms_tag1',flat=True))
    user_bad_botoms_tag2_list = list(user_bad_codnate.values_list('botoms_tag2',flat=True))
    user_bad_botoms_tag3_list = list(user_bad_codnate.values_list('botoms_tag3',flat=True))
    user_bad_botoms_tag4_list = list(user_bad_codnate.values_list('botoms_tag4',flat=True))

    user_bad_shoese_tag1_list = list(user_bad_codnate.values_list('shoese_tag1',flat=True))
    user_bad_shoese_tag2_list = list(user_bad_codnate.values_list('shoese_tag2',flat=True))
    user_bad_shoese_tag3_list = list(user_bad_codnate.values_list('shoese_tag3',flat=True))
    user_bad_shoese_tag4_list = list(user_bad_codnate.values_list('shoese_tag4',flat=True))
    



    for code_idx in range(n):
        tag_list = []
        user_like_tag_point = 0
        user_bad_tag_point = 0
        tag_list.append(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])
        
        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        tag_list.append(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])
        
        tag_list.append(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        tag1_count = tag_list.count(tag1) 
        tag2_count = tag_list.count(tag2) 
        tag3_count = tag_list.count(tag3) 
        tag4_count = tag_list.count(tag4) 



        tag_sum_list.append(tag1_count*type_match_tag_weight + tag2_count*type_match_tag_weight + tag3_count*type_match_tag_weight + tag4_count*type_match_tag_weight - type_filter_list[sorted_idx[code_idx]]*type_DCS_weight + user_like_tag_point - user_bad_tag_point)
        tag_idx_list.append(type_filter_idx_list[sorted_idx[code_idx]])
    #----------控え目か派手かで評価---------

    vol = list(user_like_type_temp.values_list('vol',flat=True))[0]

    user_photo_tops_vol_list = list(user_tops_all.values_list('vol',flat=True))
    user_photo_botoms_vol_list = list(user_botoms_all.values_list('vol',flat=True))
    user_photo_shoese_vol_list = list(user_shoese_all.values_list('vol',flat=True))
    for i in range(len(tag_sum_list)):
        vol_list = []
        vol_list.append(user_photo_tops_vol_list[tag_idx_list[i][0]])
        vol_list.append(user_photo_botoms_vol_list[tag_idx_list[i][1]])
        vol_list.append(user_photo_shoese_vol_list[tag_idx_list[i][2]])
        vol_count = vol_list.count(vol)
        tag_sum_list[i] = tag_sum_list[i] + vol_count * type_match_vol_weight
    

    tag_sorted_idx = np.argsort(tag_sum_list)[::-1]
    if 2 <= len(tag_sorted_idx):
        res_idx_list = tag_sorted_idx[0:1]
    else:
        res_idx_list = tag_sorted_idx
    #-------------一番評価の高い服を出力------------
    res_tops_path =[]
    res_botoms_path = []
    res_shoese_path = []

    res_tops_color = []
    res_botoms_color = []
    res_shoese_color = []

    res_tops_sub = []
    res_botoms_sub = []
    res_shoese_sub = []


    tops_path_list = list(user_tops_all.values_list('FilePath',flat=True))
    botoms_path_list = list(user_botoms_all.values_list('FilePath',flat=True))
    shoese_path_list = list(user_shoese_all.values_list('FilePath',flat=True))

    tops_color_list = list(user_tops_all.values_list('color',flat=True))
    botoms_color_list = list(user_botoms_all.values_list('color',flat=True))
    shoese_color_list = list(user_shoese_all.values_list('color',flat=True))

    tops_sub_list = list(user_tops_all.values_list('sub',flat=True))
    botoms_sub_list = list(user_botoms_all.values_list('sub',flat=True))
    shoese_sub_list = list(user_shoese_all.values_list('sub',flat=True))

    for i in range(len(res_idx_list)):
        res_tops_path.append(tops_path_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_color.append(tops_color_list[tag_idx_list[res_idx_list[i]][0]])
        tops_sub = tops_sub_list[tag_idx_list[res_idx_list[i]][0]]
        res_tops_sub.append(tops_sub)
            
        res_botoms_path.append(botoms_path_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_color.append(botoms_color_list[tag_idx_list[res_idx_list[i]][1]])
        botoms_sub = botoms_sub_list[tag_idx_list[res_idx_list[i]][1]]
        res_botoms_sub.append(botoms_sub)
               
        res_shoese_path.append(shoese_path_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_color.append(shoese_color_list[tag_idx_list[res_idx_list[i]][2]])
        shoese_sub = shoese_sub_list[tag_idx_list[res_idx_list[i]][2]]
        res_shoese_sub.append(shoese_sub)


    d = {
        'tops_path':res_tops_path,
        'tops_color':res_tops_color,
        'tops_sub':res_tops_sub,
        'botoms_path':res_botoms_path,
        'botoms_color':res_botoms_color,
        'botoms_sub':res_botoms_sub,
        'shoese_path':res_shoese_path,
        'shoese_color':res_shoese_color,
        'shoese_sub':res_shoese_sub,
    }
    print(d)
    return JsonResponse(d)

def get_recomend_web_item_shoese(request):
    import numpy as np

    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))

    recomend_all = models.QuerySet(Recomend_item)
    #---------ハイパーパラメータ---------
    type_DCS_weight = 1
    type_match_tag_weight = 10
    type_match_vol_weight = 10

    good_tag1_weight = 1.5
    good_tag2_weight = 1
    good_tag3_weight = 0.5
    good_tag4_weight = 0.25
    bad_tag1_weight = 1.5
    bad_tag2_weight = 1
    bad_tag3_weight = 0.5
    bad_tag4_weight = 0.25   
    #-----------------------------------
    #ユーザーの服を全部出力
    user_photo_all  = photo_all.filter(userNo=userNo)
    #カテゴリ別のクエリを抽出
    user_tops_all = user_photo_all.filter(cate='tops')
    user_botoms_all = user_photo_all.filter(cate='botoms')
    user_shoese_all = recomend_all.filter(cate='シューズ')

    tops_count = user_photo_all.filter(cate='tops').count()
    botoms_count = user_photo_all.filter(cate='botoms').count()
    shoese_count = recomend_all.filter(cate='シューズ').count()

    #アウターは冬用　まだ未開発
    outer_count = user_photo_all.filter(cate='outer').count()
    
    #服の数でコーディネートできるか判定
    if botoms_count < 1:
        return HttpResponse('botoms no item')
    if tops_count < 1:
        return HttpResponse('tops no item')


    user_type = list(models.QuerySet(Account).filter(id=userNo).values_list('type',flat=True))[0]
    print(user_type)
    #------------自分の好きなタイプのドレス率　カジュアル率　シンプル率の差が一番少ない順にする--------------
    type_temp_all = models.QuerySet(Codnate_type_temp)
    user_like_type_temp = type_temp_all.filter(code_type=user_type)
    bad_codnate_list = models.QuerySet(Bad_Codnate)

    type_dress_value = list(user_like_type_temp.values_list('dress_value',flat=True))[0]
    type_casual_value = list(user_like_type_temp.values_list('casual_value',flat=True))[0]
    type_simple_value = list(user_like_type_temp.values_list('simple_value',flat=True))[0]

    tops_dress_value_list = list(user_tops_all.values_list('dress_value',flat=True))
    tops_casual_value_list = list(user_tops_all.values_list('casual_value',flat=True))
    tops_simple_value_list = list(user_tops_all.values_list('simple_value',flat=True))

    botoms_dress_value_list = list(user_botoms_all.values_list('dress_value',flat=True))
    botoms_casual_value_list = list(user_botoms_all.values_list('casual_value',flat=True))
    botoms_simple_value_list = list(user_botoms_all.values_list('simple_value',flat=True))

    shoese_dress_value_list = list(user_shoese_all.values_list('dress_value',flat=True))
    shoese_casual_value_list = list(user_shoese_all.values_list('casual_value',flat=True))
    shoese_simple_value_list = list(user_shoese_all.values_list('simple_value',flat=True))


    type_filter_list = []
    type_filter_idx_list = []

    for tops_idx in range(tops_count):
        for botoms_idx in range(botoms_count):
            for shoese_idx in range(shoese_count):
                                
                dress_sum = tops_dress_value_list[tops_idx] + botoms_dress_value_list[botoms_idx] + shoese_dress_value_list[shoese_idx]
                casual_sum = tops_casual_value_list[tops_idx] + botoms_casual_value_list[botoms_idx] + shoese_casual_value_list[shoese_idx]
                simple_sum = tops_simple_value_list[tops_idx] + botoms_simple_value_list[botoms_idx] + shoese_simple_value_list[shoese_idx]
                dress_per = dress_sum / (dress_sum + casual_sum + simple_sum)
                casual_per = casual_sum / (dress_sum + casual_sum + simple_sum)
                simple_per = simple_sum / (dress_sum + casual_sum + simple_sum)

                type_absolute =  abs(type_dress_value - dress_per) + abs(type_casual_value - casual_per) + abs(type_simple_value - simple_per)

                type_filter_list.append(type_absolute)
                type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])

    #------------タグに一番当てはまっている組み合わせを評価-------------
    tag1 = list(user_like_type_temp.values_list('tag1',flat=True))[0]
    tag2 = list(user_like_type_temp.values_list('tag2',flat=True))[0]
    tag3 = list(user_like_type_temp.values_list('tag3',flat=True))[0]
    tag4 = list(user_like_type_temp.values_list('tag4',flat=True))[0]
    if 10 < len(type_filter_list):
        n = int(len(type_filter_list)/2)
        sorted_idx = np.argsort(type_filter_list)
    else:
        n = len(type_filter_list)
        sorted_idx = np.argsort(type_filter_list)
    tag_sum_list = []
    tag_idx_list = []

    
    user_photo_tops_tag1 = list(user_tops_all.values_list('tag',flat=True))
    user_photo_tops_tag2 = list(user_tops_all.values_list('tag2',flat=True))
    user_photo_tops_tag3 = list(user_tops_all.values_list('tag3',flat=True))
    user_photo_tops_tag4 = list(user_tops_all.values_list('tag4',flat=True))

    user_photo_botoms_tag1 = list(user_botoms_all.values_list('tag',flat=True))
    user_photo_botoms_tag2 = list(user_botoms_all.values_list('tag2',flat=True))
    user_photo_botoms_tag3 = list(user_botoms_all.values_list('tag3',flat=True))
    user_photo_botoms_tag4 = list(user_botoms_all.values_list('tag4',flat=True))

    user_photo_shoese_tag1 = list(user_shoese_all.values_list('tag',flat=True))
    user_photo_shoese_tag2 = list(user_shoese_all.values_list('tag2',flat=True))
    user_photo_shoese_tag3 = list(user_shoese_all.values_list('tag3',flat=True))
    user_photo_shoese_tag4 = list(user_shoese_all.values_list('tag4',flat=True))

    user_good_codnate = models.QuerySet(Good_Codnate).filter(userNo=userNo)

    user_like_tops_tag1_list = list(user_good_codnate.values_list('tops_tag1',flat=True))
    user_like_tops_tag2_list = list(user_good_codnate.values_list('tops_tag2',flat=True))
    user_like_tops_tag3_list = list(user_good_codnate.values_list('tops_tag3',flat=True))
    user_like_tops_tag4_list = list(user_good_codnate.values_list('tops_tag4',flat=True))

    user_like_botoms_tag1_list = list(user_good_codnate.values_list('botoms_tag1',flat=True))
    user_like_botoms_tag2_list = list(user_good_codnate.values_list('botoms_tag2',flat=True))
    user_like_botoms_tag3_list = list(user_good_codnate.values_list('botoms_tag3',flat=True))
    user_like_botoms_tag4_list = list(user_good_codnate.values_list('botoms_tag4',flat=True))

    user_like_shoese_tag1_list = list(user_good_codnate.values_list('shoese_tag1',flat=True))
    user_like_shoese_tag2_list = list(user_good_codnate.values_list('shoese_tag2',flat=True))
    user_like_shoese_tag3_list = list(user_good_codnate.values_list('shoese_tag3',flat=True))
    user_like_shoese_tag4_list = list(user_good_codnate.values_list('shoese_tag4',flat=True))

    user_bad_codnate = models.QuerySet(Bad_Codnate).filter(userNo=userNo)

    user_bad_tops_tag1_list = list(user_bad_codnate.values_list('tops_tag1',flat=True))
    user_bad_tops_tag2_list = list(user_bad_codnate.values_list('tops_tag2',flat=True))
    user_bad_tops_tag3_list = list(user_bad_codnate.values_list('tops_tag3',flat=True))
    user_bad_tops_tag4_list = list(user_bad_codnate.values_list('tops_tag4',flat=True))

    user_bad_botoms_tag1_list = list(user_bad_codnate.values_list('botoms_tag1',flat=True))
    user_bad_botoms_tag2_list = list(user_bad_codnate.values_list('botoms_tag2',flat=True))
    user_bad_botoms_tag3_list = list(user_bad_codnate.values_list('botoms_tag3',flat=True))
    user_bad_botoms_tag4_list = list(user_bad_codnate.values_list('botoms_tag4',flat=True))

    user_bad_shoese_tag1_list = list(user_bad_codnate.values_list('shoese_tag1',flat=True))
    user_bad_shoese_tag2_list = list(user_bad_codnate.values_list('shoese_tag2',flat=True))
    user_bad_shoese_tag3_list = list(user_bad_codnate.values_list('shoese_tag3',flat=True))
    user_bad_shoese_tag4_list = list(user_bad_codnate.values_list('shoese_tag4',flat=True))
    



    for code_idx in range(n):
        tag_list = []
        user_like_tag_point = 0
        user_bad_tag_point = 0
        tag_list.append(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])
        
        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_tops_tag1_list.count(user_photo_tops_tag1[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_tops_tag2_list.count(user_photo_tops_tag2[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_tops_tag3_list.count(user_photo_tops_tag3[type_filter_idx_list[sorted_idx[code_idx]][0]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_tops_tag4_list.count(user_photo_tops_tag4[type_filter_idx_list[sorted_idx[code_idx]][0]])

        tag_list.append(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_botoms_tag1_list.count(user_photo_botoms_tag1[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_botoms_tag2_list.count(user_photo_botoms_tag2[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_botoms_tag3_list.count(user_photo_botoms_tag3[type_filter_idx_list[sorted_idx[code_idx]][1]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_botoms_tag4_list.count(user_photo_botoms_tag4[type_filter_idx_list[sorted_idx[code_idx]][1]])
        
        tag_list.append(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_like_tag_point = user_like_tag_point + good_tag1_weight * user_like_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag2_weight * user_like_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag3_weight * user_like_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_like_tag_point = user_like_tag_point + good_tag4_weight * user_like_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        user_bad_tag_point = user_bad_tag_point + bad_tag1_weight * user_bad_shoese_tag1_list.count(user_photo_shoese_tag1[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag2_weight * user_bad_shoese_tag2_list.count(user_photo_shoese_tag2[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag3_weight * user_bad_shoese_tag3_list.count(user_photo_shoese_tag3[type_filter_idx_list[sorted_idx[code_idx]][2]])
        user_bad_tag_point = user_bad_tag_point + bad_tag4_weight * user_bad_shoese_tag4_list.count(user_photo_shoese_tag4[type_filter_idx_list[sorted_idx[code_idx]][2]])

        tag1_count = tag_list.count(tag1) 
        tag2_count = tag_list.count(tag2) 
        tag3_count = tag_list.count(tag3) 
        tag4_count = tag_list.count(tag4) 



        tag_sum_list.append(tag1_count*type_match_tag_weight + tag2_count*type_match_tag_weight + tag3_count*type_match_tag_weight + tag4_count*type_match_tag_weight - type_filter_list[sorted_idx[code_idx]]*type_DCS_weight + user_like_tag_point - user_bad_tag_point)
        tag_idx_list.append(type_filter_idx_list[sorted_idx[code_idx]])
    #----------控え目か派手かで評価---------

    vol = list(user_like_type_temp.values_list('vol',flat=True))[0]

    user_photo_tops_vol_list = list(user_tops_all.values_list('vol',flat=True))
    user_photo_botoms_vol_list = list(user_botoms_all.values_list('vol',flat=True))
    user_photo_shoese_vol_list = list(user_shoese_all.values_list('vol',flat=True))
    for i in range(len(tag_sum_list)):
        vol_list = []
        vol_list.append(user_photo_tops_vol_list[tag_idx_list[i][0]])
        vol_list.append(user_photo_botoms_vol_list[tag_idx_list[i][1]])
        vol_list.append(user_photo_shoese_vol_list[tag_idx_list[i][2]])
        vol_count = vol_list.count(vol)
        tag_sum_list[i] = tag_sum_list[i] + vol_count * type_match_vol_weight
    

    tag_sorted_idx = np.argsort(tag_sum_list)[::-1]
    if 2 <= len(tag_sorted_idx):
        res_idx_list = tag_sorted_idx[0:1]
    else:
        res_idx_list = tag_sorted_idx
    #-------------一番評価の高い服を出力------------
    res_tops_path =[]
    res_botoms_path = []
    res_shoese_path = []

    res_tops_color = []
    res_botoms_color = []
    res_shoese_color = []

    res_tops_sub = []
    res_botoms_sub = []
    res_shoese_sub = []


    tops_path_list = list(user_tops_all.values_list('FilePath',flat=True))
    botoms_path_list = list(user_botoms_all.values_list('FilePath',flat=True))
    shoese_path_list = list(user_shoese_all.values_list('FilePath',flat=True))

    tops_color_list = list(user_tops_all.values_list('color',flat=True))
    botoms_color_list = list(user_botoms_all.values_list('color',flat=True))
    shoese_color_list = list(user_shoese_all.values_list('color',flat=True))

    tops_sub_list = list(user_tops_all.values_list('sub',flat=True))
    botoms_sub_list = list(user_botoms_all.values_list('sub',flat=True))
    shoese_sub_list = list(user_shoese_all.values_list('sub',flat=True))

    for i in range(len(res_idx_list)):
        res_tops_path.append(tops_path_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_color.append(tops_color_list[tag_idx_list[res_idx_list[i]][0]])
        tops_sub = tops_sub_list[tag_idx_list[res_idx_list[i]][0]]
        res_tops_sub.append(tops_sub)
            
        res_botoms_path.append(botoms_path_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_color.append(botoms_color_list[tag_idx_list[res_idx_list[i]][1]])
        botoms_sub = botoms_sub_list[tag_idx_list[res_idx_list[i]][1]]
        res_botoms_sub.append(botoms_sub)
               
        res_shoese_path.append(shoese_path_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_color.append(shoese_color_list[tag_idx_list[res_idx_list[i]][2]])
        shoese_sub = shoese_sub_list[tag_idx_list[res_idx_list[i]][2]]
        res_shoese_sub.append(shoese_sub)


    d = {
        'tops_path':res_tops_path,
        'tops_color':res_tops_color,
        'tops_sub':res_tops_sub,
        'botoms_path':res_botoms_path,
        'botoms_color':res_botoms_color,
        'botoms_sub':res_botoms_sub,
        'shoese_path':res_shoese_path,
        'shoese_color':res_shoese_color,
        'shoese_sub':res_shoese_sub,
    }
    print(d)
    return JsonResponse(d)

def get_recomend_item_list(request):
    import numpy as np
    user_id = request.GET.get('UserNo')
    user_type = list(models.QuerySet(Account).filter(id=user_id).values_list('type',flat=True))[0]
    print(user_type)
    type_value = models.QuerySet(Codnate_type_temp).filter(code_type=user_type).first()
    dress_value = type_value.dress_value
    casual_value = type_value.casual_value
    simple_value = type_value.simple_value

    tag1 = type_value.tag1
    tag2 = type_value.tag2
    tag3 = type_value.tag3
    tag4 = type_value.tag4
    vol = type_value.vol

    recomend_item = models.QuerySet(Recomend_item).all()

    recomend_dress_value =  np.array(list(recomend_item.values_list('dress_value',flat=True)))
    recomend_casual_value = np.array(list(recomend_item.values_list('casual_value',flat=True)))
    recomend_simple_value = np.array(list(recomend_item.values_list('simple_value',flat=True)))
    recomend_dress_value = abs(recomend_dress_value-dress_value)
    recomend_casual_value = abs(recomend_casual_value-casual_value)
    recomend_simple_value = abs(recomend_simple_value-simple_value)

    range_list = recomend_dress_value + recomend_casual_value + recomend_simple_value
    
    recomend_idx = range_list.argsort()

    link_url = list(recomend_item.values_list('url',flat=True))
    image_url = list(recomend_item.values_list('FilePath',flat=True))
    sub = list(recomend_item.values_list().values_list('sub',flat=True))
    price = list(recomend_item.values_list().values_list('price',flat=True))

    select_link_url = []
    select_image_url = []
    select_sub = []
    select_price = []
    for i in recomend_idx:
        select_link_url.append(link_url[i])
        select_image_url.append(image_url[i])
        select_sub.append(sub[i])
        select_price.append(price[i])
    d = {'link_url':select_link_url,
         'image_url':select_image_url,
         'sub':select_sub,
         'price':select_price}
    print(d)
    return JsonResponse(d)
    """
    return HttpResponse('{'+
                          '"link_url":'+str(select_link_url)+','+
                          '"image_url":'+str(select_image_url)+','+
                          '"sub":'+str(select_sub)+','+
                          '"price":'+str(select_price)+','+
                          '}')
"""

@csrf_exempt
def post_shop_info(request):
    if request.method == "GET":
        return HttpResponse("conection error")
    else:
        name = request.POST['name']
        latitube = float(request.POST['latitube'])
        longitube = float(request.POST['longitube'])

        shop = Local_shop(name=name,latitube=latitube,longitube=longitube)
        shop.save()

        return HttpResponse('shop save')

 

def get_recomend_local_item(request):
    userNo = request.GET.get('userNo')
    myAccount = models.QuerySet(Account).filter(id=userNo)

    x = request.GET.get('x')
    y = request.GET.get('y')



@csrf_exempt
def bad_codnate_delete(request):
    if request.method == 'GET':
        return HttpResponse()
    try:
        userNo = request.POST['user_no']
        tops_path = request.POST['tops_path']
        botoms_path = request.POST['botoms_path']
        shoese_path = request.POST['shoese_path']

        bad_codnate_list = models.QuerySet(Bad_Codnate)
        bad_codnate_list.filter(userNo=userNo,tops_path=tops_path,botoms_path=botoms_path,shoese_path=shoese_path).delete()
        return HttpResponse("delete complete")
    except Exception:
        return HttpResponse("totyu de error")
@csrf_exempt
def getCate(request):
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb

    if request.method == 'GET':
        return HttpResponse("error")
    else:
        if request.FILES is None:
            return HttpResponse("no File error")
        photoForm = PhotoOneForm(request.POST,request.FILES)
        if not photoForm.is_valid():
            raise ValueError("invaled error")

        print(request.POST)
        img = photoForm.cleaned_data['image']

        
        tb._SYMBOLIC_SCOPE.value = True

        model_cate = Mynet(4);
        model_cate.load_weights('/home/ubuntu/codnate_jango/tanuki/huku.h5')
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        path = '/home/ubuntu/codnate_jango'+photo_one.photo.url
        img = cv2.imread(path,1)

        #cate_label = ['トップス','ワンピース','アウター','ボトムス']
        cate_label = ['tops','onepeace','outer','botoms','shoese']
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255
        #モデルに掛ける（チェック）
        pred = model_cate.predict(cutx,1,0)
        label = np.argmax(pred)
        score = np.max(pred)
        
        K.clear_session()
        print('score'+str(pred))
        print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_label[label])
        if score <=0.3:
            label =4

        print(path)
        return HttpResponse(cate_label[label]+','+path)
@csrf_exempt
def getColor(request):
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb
    if request.method == 'GET':
        return HttpResponse("error")
    else:
        photoForm = PhotoOneForm(request.POST,request.FILES)
        if not photoForm.is_valid():
            raise ValueError("invaled error")

        print(request.POST)
        img = photoForm.cleaned_data['image']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        path = '/home/ubuntu/codnate_jango'+photo_one.photo.url
        
        img = cv2.imread(path,1)        
        tb._SYMBOLIC_SCOPE.value = True
        print('path:'+path)
        print('mynet')
        model_cate = Mynet(11);
        model_cate.load_weights('/home/ubuntu/codnate_jango/tanuki/color.h5')
        
        cate_label = ['black','blue','brown','gray','green','orange','pink','purple','red','white','yellow']
        #cate_label = ['white','black','blue','brown','gray','green','orange','pink','purple','red','yellow']
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255
        #モデルに掛ける（チェック）
        pred = model_cate.predict(cutx,1,0)
        label = np.argmax(pred)
        score = np.max(pred)
        
        K.clear_session()

        print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_label[label])
        return HttpResponse(cate_label[label]+','+path)
@csrf_exempt
def getsubCate(request):
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb   
   
    import random
    
    
    if request.method == 'GET':
        return HttpResponse("error")
    else:

        
        tb._SYMBOLIC_SCOPE.value = True
        path = request.POST['path']        
        sub = request.POST['cate']
        
        img = cv2.imread(path,cv2.IMREAD_COLOR)

        
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255
        #tops
        if sub == 'tops':
            model_tops = Mynet(5)
            model_tops.load_weights('/home/ubuntu/codnate_jango/tanuki/tops.h5')
            #cate_name=['ブラウス_チュニック',
             #          'ビスチェ_キャミソール_タンクトップ',
              #         'カットソー_ニット_オフショルダー',
               #        'スウェット_セーター_パーカー',
                #       'シャツ_Ｔシャツ_ポロシャツ']
            cate_name =['blouse_tunic',
                        'busiter_camisole_tanktop',
                        'cut-and-saw_knit_offshoulder',
                        'swrat_sweater_parker',
                        'shirt_t-shirt_poloshirt']
            #モデルに掛ける（チェック）
            pred = model_tops.predict(cutx,1,0)
            label = np.argmax(pred)
            score = np.max(pred)
            print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_name[label])
            K.clear_session()

            return HttpResponse(cate_name[label])

        #onepeace
        elif sub == 'onepeace':
            model_onepeace = Mynet(5)
            model_onepeace.load_weights('/home/ubuntu/codnate_jango/tanuki/onepeace.h5')
        
            #cate_name=['ドレス',
             #         'キャミドレス_マキシ丈ドレス',
              #         'ワンピース_ひざ丈ドレス_ミニドレス',
               #        'サロペット_コンビネゾン_オーバーオール',
                #       'シャツドレス_ニットドレス']
            cate_name=['dress',
                       'camisole_maxidress',
                      'onepeace_knee-lengthdress',
                     'saropetto_convenience_overalls',
                       'shirtdress_nittodress']
            #モデルに掛ける（チェック）
            pred = model_onepeace.predict(cutx,1,0)
            label = np.argmax(pred)
            score = np.max(pred)
            print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_name[label])
            K.clear_session()

            return HttpResponse(cate_name[label])
               
        #outer
        elif sub == 'outer':
            model_outer = Mynet(9)
            model_outer.load_weights('/home/ubuntu/codnate_jango/tanuki/outer.h5')
        
            #cate_name=['ポンチョ',
             #          'カーディガン',
              #         'ファーコート',
               #        'ジャケット',
                #       'MA1_ブルゾン_ミリタリージャケット',
                 #      'マウンテンパーカー',
                  #     'ダウンコート_ダウンベスト',
                   #    'デニムジャケット_レザージャケット',
                    #   'チェスターコート_ピーコート_ダッフルコート']
            cate_name=['boncho',
                       'cardigan',
                       'hur-coat',
                       'jacket',
                       'ma1_blouson_military-acket',
                       'moutain-perker_mods-coat_raincoat',
                       'down-coat_down-vest',
                       'denim-jacket_leather-jacket',
                       'chester-coat_pcoat_duffle-coat']

            #モデルに掛ける（チェック）
            pred = model_outer.predict(cutx,1,0)
            label = np.argmax(pred)
            score = np.max(pred)
            print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_name[label])
            K.clear_session()


            return HttpResponse(cate_name[label])
        #botoms
        elif sub == 'botoms':
            model_botoms = Mynet(8)
            model_botoms.load_weights('/home/ubuntu/codnate_jango/tanuki/botoms.h5')
        
            #cate_name=['カーゴパンツ',
             #          'タイトスカート',
              #         'デニム_スキニーパンツ_スウェットパンツ',
               #        'デニムスカート_ミニスカート',
                #       'フレアスカート_プリーツスカート',
                 #      'ハーフパンツ',
                  #     'マキシ丈スカート_ミモレスカート',
                   #    'タックパンツ_ワイドパンツ']
            
            cate_name = ['cargopants',
                         'tightskirt',
                         'denim_skinnypants_sweatpants',
                         'denimskirt_miniskirt',
                         'flareskirt_pleatedskirt_tuleskirt',
                         'harfpants',
                         'maxilengthskirt_mimoreskirt',
                         'tuckpants_widepants']
            #モデルに掛ける（チェック）
            pred = model_botoms.predict(cutx,1,0)
            label = np.argmax(pred)
            score = np.max(pred)
            print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_name[label])
            K.clear_session()
            return HttpResponse(cate_name[label])

        elif sub == 'shoese':
            
            cate_name = ['sandals_beacesandal_mules',
                         'booty_boots_rainshoese',
                         'sneakers_moccasin',
                         'slipons',
                         'loafer_pumps_dressshoese',
                         ]
                         
            return HttpResponse(cate_name[int(random.uniform(0,4))])
@csrf_exempt
def get_type(request):
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb
    
    
    if request.method == 'GET':
        return HttpResponse("error")
    else:
                
        
        tb._SYMBOLIC_SCOPE.value = True
        path = request.POST['path']
        
        img = cv2.imread(path,1)

        cate_label = ['simmple','casual','dress']
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255

        model_casual = Mynet(3)
        model_casual.load_weights('/home/ubuntu/codnate_jango/tanuki/casu_dre.h5')

        pred = model_casual.predict(cutx,1,0)
        label = np.argmax(pred)
        score = np.max(pred)
        print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_label[label])
        K.clear_session()
        print(pred)
        return HttpResponse(str(int(pred[0][0]*100))+','+str(int(pred[0][1]*100))+','+str(int(pred[0][2]*100)))
@csrf_exempt
def get_tag(request):
    
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb
    
    if request.method == 'GET':
        return HttpResponse("error")
    else:
        photoForm = PhotoOneForm(request.POST,request.FILES)
        if not photoForm.is_valid():
            raise ValueError("invaled error")

        print(request.POST)
        img = photoForm.cleaned_data['image']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        path = '/home/ubuntu/codnate_jango'+photo_one.photo.url

        tb._SYMBOLIC_SCOPE.value = True
        
        
        img = cv2.imread(path,1)

        #cate_label = ['ワイルド','ゆるい','かっこいい','かわいい','大人っぽい','子供っぽい','きれい','ふわふわ']
        #cate_label = ['wild','yurui','cool','kawaii','adult','child','beuty','huwahuwa']
        cate_label = ['cool','kawaii','adult','wild','yurui','child','beuty','huwahuwa']
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255

        model_casual = Mynet(8)
        model_casual.load_weights('/home/ubuntu/codnate_jango/tanuki/tag_list.h5')

        pred = model_casual.predict(cutx,1,0)
        label = np.argmax(pred)
        score = np.max(pred)
        label_np = np.array(pred)
        label_sort = label_np.argsort()[::-1]
        print(label_sort)
        print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_label[label])
        K.clear_session()
        
        return HttpResponse(cate_label[label_sort[0][0]]+','+cate_label[label_sort[0][1]]+','+cate_label[label_sort[0][2]]+','+cate_label[label_sort[0][3]]+','+path)
@csrf_exempt
def get_vol(request):

    
    import cv2
    import numpy as np
    from keras import backend as K 
    import keras.backend.tensorflow_backend as tb
    if request.method == 'GET':
        return HttpResponse("error")
    else:
        tb._SYMBOLIC_SCOPE.value = True

        path = request.POST['path']
        img = cv2.imread(path,1)

        #cate_label = ['控えめ','派手']
        cate_label = ['hikaeme','hade']
        #画像をリサイズ（今回は64）
        cutx = cv2.resize(img,(64,64))
        #画像の色をRGB形式に変更
        cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
        #次元数を上げる
        cutx = cutx.reshape((1,)+cutx.shape)
        cutx /= 255

        model_casual = Mynet(2)
        model_casual.load_weights('/home/ubuntu/codnate_jango/tanuki/vol.h5')

        pred = model_casual.predict(cutx,1,0)
        label = np.argmax(pred)
        score = np.max(pred)
        print('label:'+str(label)+' score:'+str(score)+' cate:'+cate_label[label])
        K.clear_session()
        
        hikaeme = int(pred[0][0]*100)
        hade = int(pred[0][1]*100)
        return HttpResponse(str(hikaeme)+','+str(int(hade)))
def Mynet(cate_num):
    import numpy as np
    from keras.models import Sequential
    from keras.layers.convolutional import MaxPooling2D
    from keras.layers import Activation , Conv2D , Flatten , Dense , Dropout
    img_height, img_width = 64,64

        #~~~~~１層~~~~~#
    #訓練レイヤーが扱える関数を格納(損失値や評価、重みづけなど))
    model = Sequential()

    #畳み込み層を追加　32行になるように　3×3の畳み込み係数（カーネル）を使い
    #ゼロパディングを追加して出力後のデータが元の大きさになるように　画像を出力していく　
    model.add(Conv2D(32, (3, 3), padding = 'same',input_shape=(img_height,img_width,3)))

    #活性化関数を追加　「relu」は微分を行う(マイナスならば0 プラスならばそのまま))
    model.add(Activation('relu'))

    #32行になるように畳み込みを行う(長方形の行列から正方形の行列になるように)
    model.add(Conv2D(32,(3,3)))

    #もう一度微分
    model.add(Activation('relu'))

    #画像のスケールダウンを行う(垂直、水平)
    model.add(MaxPooling2D(pool_size=(2,2)))

    #0.25以下の数をなくす　これにより計算の数が減少
    model.add(Dropout(0.25))

    #~~~~~２層~~~~~#
    #64行に増やしていく
    model.add(Conv2D(64, (3, 3), padding = 'same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.375))

    #~~~~~３層~~~~~#
    #多次元配列を平らにする 
    #もとは４次元テンソル(画像のサンプル数、画像のチャネル数（色情報)、画像の縦幅、画像の横幅）を１次元に落とし込む
    model.add(Flatten())

    #512行の行列として出力
    model.add(Dense(512))

    #微分する
    model.add(Activation('relu'))

    #0.5以下のやつを省く
    model.add(Dropout(0.5))

    #フォルダ数と同じ行列にして出力
    model.add(Dense(cate_num))
    #ソフトマックス関数 ここで隠れ層を通過し、確率を表す数字が出てきたところで「全体から見て何割の確率か」を算出する
    model.add(Activation('softmax'))

    return model



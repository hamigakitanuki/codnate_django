from django.shortcuts import render
from django.http import HttpResponse
from .models import Photo,Account,BlackList,Sub_type_value,Color_type_value
import json
from django.db import models
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.shortcuts import get_current_site
import re
from django.core.files import File
from django.db.models import Max
from .forms import PhotoForm,AccountForm
from django.views.decorators.csrf import csrf_exempt
import random

#テスト用
def index(request):
    return HttpResponse("hallo django")

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
        prin = models.QuerySet(Sub_type_value).get(sub=sub)
        print(prin)
        #画像をDBに登録
        photo = Photo(userNo=userNo,FileName=filename,file=form.cleaned_data['image'],
                      cate=cate,sub=sub,color=color,sub_type_value=models.QuerySet(Sub_type_value).get(sub=sub),
                      color_type_value=models.QuerySet(Color_type_value).get(color=color))
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
    sub_type_value_list1 = list(ac.values_list('Sub_type_value.type1',flat=True))
    sub_type_value_list2 = list(ac.values_list('Sub_type_value.type2',flat=True))
    color_type_value_list = list(ac.values_list('Color_type_value.type',flat=True))

    

    print(path_list)
    #dict型にする
    d = {
        'path_list' :path_list,
        'cate_list' :cate_list,
        'sub_list'  :sub_list,
        'color_list':color_list,
        'sub_type_value_list1':sub_type_value_list1,
        'sub_type_value_list2':sub_type_value_list2,
        'color_type_value_list':color_type_value_list,

    }
    return JsonResponse(d)

def getCodenate(request):
    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))
    #ユーザーの服を全部出力
    photo_all  = photo_all.filter(userNo=userNo)
    #サブカテゴリとファイルパスを出力
    photo_tops_sub = list(photo_all.filter(cate='トップス').values_list('sub',flat=True))
    photo_tops_path = list(photo_all.filter(cate='トップス').values_list('FilePath',flat=True))
    #ブラックリストを出力
    blackList = models.QuerySet(BlackList)

    tops_path = []
    botoms_path = []
    outer_path = []
    shoese_path = []

    for i in range(3):
        #トップスからランダムで出力
        tops_idx = random.randint(0,len(photo_tops_sub)-1)

        #ブラックリストで除外するボトムスをリスト形式で出力
        tops_out_list = list(blackList.filter(sub1=photo_tops_sub[tops_idx]).values_list('sub2',flat=True))
        print(tops_out_list)
        
        #ボトムスのサブカテゴリリストから除外して出力するものだけを残す
        photo_botoms_sub = list(photo_all.filter(cate='ボトムス').values_list('sub',flat=True))
        if len(photo_botoms_sub) >=1:
            photo_botoms_sub = [s for s in photo_botoms_sub if s != tops_out_list[:]]

            photo_botoms_sub = list(photo_all.filter(sub__in=photo_botoms_sub).values_list('sub',flat=True))
            photo_botoms_path = list(photo_all.filter(sub__in=photo_botoms_sub).values_list('FilePath',flat=True))
            #ボトムスからランダムで出力
            if len(photo_botoms_path) >= 1:
                botoms_idx = random.randint(0,len(photo_botoms_path)-1)
                botoms_path.append(photo_botoms_path[botoms_idx])
                botoms_out_list = list(blackList.filter(sub1=photo_botoms_sub[botoms_idx]).values_list('sub2',flat=True))

        
        #アウターのサブカテゴリリストから除外して出力するものだけを残す
        photo_outer_sub = list(photo_all.filter(cate='アウター').values_list('sub',flat=True))
        if len(photo_outer_sub) >= 1:
            photo_outer_sub = [s for s in photo_outer_sub if s != tops_out_list[:]]

            photo_outer_sub = list(photo_all.filter(sub__in=photo_outer_sub).values_list('sub',flat=True))
            photo_outer_path = list(photo_all.filter(sub__in=photo_outer_sub).values_list('FilePath',flat=True))
            #アウターからランダムで出力       
            if len(photo_outer_path) >= 1:
                outer_idx = random.randint(0,len(photo_outer_path)-1)
                outer_path.append(photo_outer_path[outer_idx])
                outer_out_list = list(blackList.filter(sub1=photo_outer_sub[outer_idx]).values_list('sub2',flat=True))


        #シューズのサブカテゴリリストから除外して出力するものだけを残す
        photo_shoese_sub = list(photo_all.filter(cate='シューズ').values_list('sub',flat=True))
        if len(photo_shoese_sub) >= 1:
            photo_shoese_sub = [s for s in photo_shoese_sub if s != tops_out_list[:]]

            photo_shoese_path = list(photo_all.filter(sub__in=photo_shoese_sub).values_list('sub',flat=True))
            photo_shoese_path = list(photo_all.filter(sub__in=photo_shoese_sub).values_list('FilePath',flat=True))
            #シューズからランダムで出力
            if len(photo_shoese_path) >= 1:
                shoese_idx = random.randint(0,len(photo_shoese_path)-1)
                shoese_path.append(photo_shoese_path[shoese_idx])
                shoese_out_list = list(blackList.filter(sub1=photo_shoese_sub[shoese_idx]).values_list('sub2',flat=True))
        
        tops_path.append(photo_tops_path[tops_idx])
        
    
    d = {"tops_path":tops_path,
         "botoms_path":botoms_path,
         "outer_path":outer_path,
         "shoese_path":shoese_path}
    print(d)
    return JsonResponse(d)


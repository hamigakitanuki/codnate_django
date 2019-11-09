from django.shortcuts import render
from django.http import HttpResponse
from .models import Photo,Account
import json
from django.db import models
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.shortcuts import get_current_site
import re
from django.core.files import File
from django.db.models import Max
from .forms import PhotoForm
from django.views.decorators.csrf import csrf_exempt

#テスト用
def index(request):
    return HttpResponse("hallo django")

"""
"""
@ensure_csrf_cookie
def newAccount(requset):
    if requset == 'GET':
        return HttpResponse({})
    try:
        ac = Account(name=requset.GET.get('name'),
                     sex=requset.GET.get('sex'),
                     age=requset.GET.get('age'),
                     type=requset.GET.get('type'))
        ac.save()
        UserNo = models.QuerySet(Account).all().aggregate(Max('id'))
        HttpResponse(UserNo)
    except Exception:
        HttpResponse('totyudeerror')
        
#画像のPOST用　userNoとファイルとファイル名がセットで来る

def imgInDB(request):
    
    #GETだった場合
    if request == 'GET':
        return HttpResponse({})
    
    try:
        #ファイルが入っているか確認
        if request.FILES == None:
            HttpResponse('error')
        #アップロードされたファイルを変数に格納
        form = PhotoForm(request.POST,request.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')        
        filename = str(form.cleaned_data['image'])
        userNo = re.split('_',filename)
        userNo = int(userNo[0])

        #画像をDBに登録
        photo = Photo(userNo=userNo,FileName=filename,file=form.cleaned_data['image'])
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

"""
"""

#画像のGET専用
def getImage(request):
    #それぞれを抽出(UserNo以外配列)
    userNo = request.GET.get('UserNo')
    cate = request.GET.get('cate')
    sub = request.GET.get('sub')
    color = request.GET.get('color')
    
    #UserNoがない場合はエラー
    if(userNo == 'None'):
        HttpResponse('UserNo None')
    #画像のクエリ作成
    ac = models.QuerySet(Photo)
    #画像からUserNoで抽出
    ac =  ac.filter(userNo = userNo)
    #カテゴリで選別
    if(cate != 'None'):
        ac = ac.filter(cate = cate)
    if(sub != 'None'):
        ac = ac.filter(sub = cate)
    if(color != 'None'):
        ac = ac.filter(color = cate)
    
    #クエリをリスト型にする 画像のあるURLを送る
    path_list = list(ac.values_list('FilePath',flat=True))
    cate_list = list(ac.values_list('cate',flat=True))

    print(path_list)
    #dict型にする
    d = {
        'path_list':path_list
    }
    return JsonResponse(d)
    #画像のURLをまとめて送る
    #return render(request,'tanuki/imagePath.html',context=d)
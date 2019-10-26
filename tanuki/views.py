from django.shortcuts import render
from django.http import HttpResponse
from .models import Photo
import json
from django.db import models
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.shortcuts import get_current_site
import re
from django.core.files import File

#テスト用
def index(request):
    return render(request,'tanuki/form.html')

"""
"""

#画像のPOST用　userNoとファイルとファイル名がセットで来る
@ensure_csrf_cookie
def imgInDB(request):
    
    #GETだった場合
    if request == 'GET':
        return HttpResponse({})
    
    try:
        #ファイルが入っているか確認
        if request.FILES == None:
            HttpResponse('none file')
        #アップロードされたファイルを変数に格納
        upload_file = request.FILES['file']
        
        FileName = str(upload_file)
        print(FileName)
        userNo = re.split('_',FileName)
        print(userNo)
        userNo = int(userNo[0])
        print(userNo)
        #画像をDBに登録
        photo = Photo(userNo=userNo,FileName=FileName,file=upload_file)
        print('user')
        photo.save()
        print('db')
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
        print(download_url)
        #DBの画像のURLを更新
        photo = models.QuerySet(Photo)
        print(1)
        photo_obj = photo.filter(FileName=FileName).first()
        print(photo_obj)
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
    
    if(userNo == 'None'):
        HttpResponse('UserNo None')
    #画像のクエリ作成
    ac = models.QuerySet(Photo)
    #画像からUserNoで抽出
    ac =  ac.filter(userNo = userNo)

    #クエリをリスト型にする
    path_list = list(ac.values_list('FilePath',flat=True))
    print(path_list)
    #dict型にする
    d = {
        'path_list':path_list
    }
    return JsonResponse(d)
    #画像のURLをまとめて送る
    #return render(request,'tanuki/imagePath.html',context=d)
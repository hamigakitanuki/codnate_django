from django.shortcuts import render
from django.http import HttpResponse
from .models import Photo,Account,Photo_one,Codnate_type_temp,Bad_Codnate,Good_Codnate
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

def getCodenate(request):
    import numpy as np

    userNo = request.GET.get('UserNo')
    photo_all = models.QuerySet(Photo)
    print(str(userNo))
    #ユーザーの服を全部出力
    user_photo_all  = photo_all.filter(userNo=userNo)
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
    print(user_type)
#------------自分の好きなタイプのドレス率　カジュアル率　シンプル率の差が一番少ない順にする--------------
    type_temp_all = models.QuerySet(Codnate_type_temp)
    user_like_type_temp = type_temp_all.filter(code_type=user_type)
    bad_codnate_list = models.QuerySet(Bad_Codnate)

    type_dress_value = list(user_like_type_temp.values_list('dress_value',flat=True))[0]
    type_casual_value = list(user_like_type_temp.values_list('casual_value',flat=True))[0]
    type_simple_value = list(user_like_type_temp.values_list('simple_value',flat=True))[0]
    
    tops_path_list = list(user_photo_all.filter(cate='tops').values_list('FilePath',flat=True))
    botoms_path_list = list(user_photo_all.filter(cate='botoms').values_list('FilePath',flat=True))
    shoese_path_list = list(user_photo_all.filter(cate='shoese').values_list('FilePath',flat=True))
    

    tops_dress_value_list = list(user_photo_all.filter(cate='tops').values_list('dress_value',flat=True))
    tops_casual_value_list = list(user_photo_all.filter(cate='tops').values_list('casual_value',flat=True))
    tops_simple_value_list = list(user_photo_all.filter(cate='tops').values_list('simple_value',flat=True))

    botoms_dress_value_list = list(user_photo_all.filter(cate='botoms').values_list('dress_value',flat=True))
    botoms_casual_value_list = list(user_photo_all.filter(cate='botoms').values_list('casual_value',flat=True))
    botoms_simple_value_list = list(user_photo_all.filter(cate='botoms').values_list('simple_value',flat=True))

    shoese_dress_value_list = list(user_photo_all.filter(cate='shoese').values_list('dress_value',flat=True))
    shoese_casual_value_list = list(user_photo_all.filter(cate='shoese').values_list('casual_value',flat=True))
    shoese_simple_value_list = list(user_photo_all.filter(cate='shoese').values_list('simple_value',flat=True))


    type_filter_list = []
    type_filter_idx_list = []

    for tops_idx in range(tops_count):
        for botoms_idx in range(botoms_count):
            for shoese_idx in range(shoese_count):
                
                if bad_codnate_list.filter(tops_path=tops_path_list[tops_idx],
                                           botoms_path=botoms_path_list[botoms_idx],
                                           shoese_path=shoese_path_list[shoese_idx]).count() > 0:
                    type_filter_list.append(999)
                    type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])
                    continue
                
                dress_sum = tops_dress_value_list[tops_idx] + botoms_dress_value_list[botoms_idx] + shoese_dress_value_list[shoese_idx]
                casual_sum = tops_casual_value_list[tops_idx] + botoms_casual_value_list[botoms_idx] + shoese_casual_value_list[shoese_idx]
                simple_sum = tops_simple_value_list[tops_idx] + botoms_simple_value_list[botoms_idx] + shoese_simple_value_list[shoese_idx]
                dress_per = dress_sum / (dress_sum + casual_sum + simple_sum)
                casual_per = casual_sum / (dress_sum + casual_sum + simple_sum)
                simple_per = simple_sum / (dress_sum + casual_sum + simple_sum)

                type_absolute =  abs(type_dress_value - dress_per) + abs(type_casual_value - casual_per) + abs(type_simple_value - simple_per)

                type_filter_list.append(type_absolute)
                type_filter_idx_list.append([tops_idx,botoms_idx,shoese_idx])

                print(type_absolute)
    print(type_filter_list)
    print(type_filter_idx_list)
#------------タグに一番当てはまっている組み合わせを選択する-------------
    tag1 = list(user_like_type_temp.values_list('tag1',flat=True))[0]
    tag2 = list(user_like_type_temp.values_list('tag2',flat=True))[0]
    tag3 = list(user_like_type_temp.values_list('tag3',flat=True))[0]
    tag4 = list(user_like_type_temp.values_list('tag4',flat=True))[0]
    print("tag1:"+tag1)
    print("tag2:"+tag2)
    print("tag3:"+tag3)
    print("tag4:"+tag4)
    if 5 < len(type_filter_list):
        n = 5
        sorted_idx = np.argsort(type_filter_list)
    else:
        n = len(type_filter_list)
        sorted_idx = np.argsort(type_filter_list)
    tag_sum_list = []
    tag_idx_list = []

    print(sorted_idx)
    
    for code_idx in range(n):
        tag_list = []
        
        tag_list.append(list(user_photo_all.filter(cate='tops').values_list('tag',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(list(user_photo_all.filter(cate='tops').values_list('tag2',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(list(user_photo_all.filter(cate='tops').values_list('tag3',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][0]])
        tag_list.append(list(user_photo_all.filter(cate='tops').values_list('tag4',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][0]])
        
        tag_list.append(list(user_photo_all.filter(cate='botoms').values_list('tag',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(list(user_photo_all.filter(cate='botoms').values_list('tag2',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(list(user_photo_all.filter(cate='botoms').values_list('tag3',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][1]])
        tag_list.append(list(user_photo_all.filter(cate='botoms').values_list('tag4',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][1]])

        tag_list.append(list(user_photo_all.filter(cate='shoese').values_list('tag',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(list(user_photo_all.filter(cate='shoese').values_list('tag2',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(list(user_photo_all.filter(cate='shoese').values_list('tag3',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][2]])
        tag_list.append(list(user_photo_all.filter(cate='shoese').values_list('tag4',flat=True))[type_filter_idx_list[sorted_idx[code_idx]][2]])
        print(tag_list)
        tag1_count = tag_list.count(tag1) 
        tag2_count = tag_list.count(tag2) 
        tag3_count = tag_list.count(tag3) 
        tag4_count = tag_list.count(tag4) 

        tag_sum_list.append(tag1_count*10 + tag2_count*10 + tag3_count*10 + tag4_count*10 - type_filter_list[sorted_idx[code_idx]])
        tag_idx_list.append(type_filter_idx_list[sorted_idx[code_idx]])
        print("300----------->"+str(tag_sum_list))

#----------控え目か派手かで選択---------
    


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

    tops_path_list = list(user_photo_all.filter(cate='tops').values_list('FilePath',flat=True))
    botoms_path_list = list(user_photo_all.filter(cate='botoms').values_list('FilePath',flat=True))
    shoese_path_list = list(user_photo_all.filter(cate='shoese').values_list('FilePath',flat=True))

    tops_color_list = list(user_photo_all.filter(cate='tops').values_list('color',flat=True))
    botoms_color_list = list(user_photo_all.filter(cate='botoms').values_list('color',flat=True))
    shoese_color_list = list(user_photo_all.filter(cate='shoese').values_list('color',flat=True))

    tops_sub_list = list(user_photo_all.filter(cate='tops').values_list('sub',flat=True))
    botoms_sub_list = list(user_photo_all.filter(cate='botoms').values_list('sub',flat=True))
    shoese_sub_list = list(user_photo_all.filter(cate='shoese').values_list('sub',flat=True))
    print('331----------->'+str(len(res_idx_list)))
    for i in range(len(res_idx_list)):
        res_tops_path.append(tops_path_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_color.append(tops_color_list[tag_idx_list[res_idx_list[i]][0]])
        res_tops_sub.append(tops_sub_list[tag_idx_list[res_idx_list[i]][0]])
            
        res_botoms_path.append(botoms_path_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_color.append(botoms_color_list[tag_idx_list[res_idx_list[i]][1]])
        res_botoms_sub.append(botoms_sub_list[tag_idx_list[res_idx_list[i]][1]])
               
        res_shoese_path.append(shoese_path_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_color.append(shoese_color_list[tag_idx_list[res_idx_list[i]][2]])
        res_shoese_sub.append(shoese_sub_list[tag_idx_list[res_idx_list[i]][2]])

    d = {
        'tops_path':res_tops_path,
        'tops_color':res_tops_color,
        'tops_sub':res_tops_sub,
        'botoms_path':res_botoms_path,
        'botoms_color':res_botoms_color,
        'botoms_sub':res_botoms_sub,
        'shoese_path':res_shoese_path,
        'shoese_color':res_shoese_color,
        'shoese_sub':res_shoese_sub
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

        bad = Bad_Codnate(userNo=userNo,tops_path=tops_path,botoms_path=botoms_path,shoese_path=shoese_path)
        bad.save()

        return HttpResponse('bad complete')
    except Exception:
        return HttpResponse('totyuude error')
@csrg_exempt
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
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,1)

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
        return HttpResponse(cate_label[label])
@csrf_exempt
def getColor(request):
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

        print('mynet')
        model_cate = Mynet(11);
        model_cate.load_weights('/home/ubuntu/codnate_jango/tanuki/color.h5')
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,1)
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
        return HttpResponse(cate_label[label])
@csrf_exempt
def getsubCate(request):
    
    import cv2
    import numpy as np
    import keras.backend.tensorflow_backend as tb
    from keras import backend as K 
    import random
    
    
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
        
        sub = request.POST['sub']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        print(photo_one.photo.url)
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,cv2.IMREAD_COLOR)

        
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
    import keras.backend.tensorflow_backend as tb
    from keras import backend as K 
    
    
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
        
        sub = request.POST['sub']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,1)

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
    import keras.backend.tensorflow_backend as tb
    from keras import backend as K 
    
    
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
        
        sub = request.POST['sub']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,1)

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
        
        return HttpResponse(cate_label[label_sort[0][0]]+','+cate_label[label_sort[0][1]]+','+cate_label[label_sort[0][2]]+','+cate_label[label_sort[0][3]])
@csrf_exempt
def get_vol(request):
    import cv2
    import numpy as np
    import keras.backend.tensorflow_backend as tb
    from keras import backend as K 
    
    
    if request.method == 'GET':
        return HttpResponse("error")
    else:
        if request.FILES is None:
            return HttpResponse("no File error")
        photoForm = PhotoOneForm(request.POST,request.FILES)
        if not photoForm.is_valid():
            raise ValueError("invaled error")

        img = photoForm.cleaned_data['image']

        
        tb._SYMBOLIC_SCOPE.value = True
        
        sub = request.POST['sub']
        
        photo_one = Photo_one(photo=img)
        photo_one.save()
        img = cv2.imread('/home/ubuntu/codnate_jango/'+photo_one.photo.url,1)

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
        
        return HttpResponse(str(int(pred[0][0]*100))+','+str(int(pred[0][1]*100)))
def Mynet(cate_num):
    import cv2
    from sklearn.model_selection import train_test_split
    from keras.optimizers import SGD , Adadelta
    import numpy as np
    from keras.preprocessing.image import ImageDataGenerator
    from PIL import Image
    from collections import Counter
    import os
    import tensorflow as tf
    from keras import backend as K 
    from keras.utils import np_utils
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



import cv2
import numpy as np    
import csv
import requests
from keras import backend as K 

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



model_color = Mynet(11);
model_color.load_weights('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/color.h5')

model_vol = Mynet(2)
model_vol.load_weights('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/vol.h5')

model_dre = Mynet(3)
model_dre.load_weights('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/casu_dre.h5')

model_tag = Mynet(8)
model_tag.load_weights('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/tag_list.h5')

tag_label = ["huwahuwa","beuty", "child","adult","kawaii","cool","yurui","wild"]
color_label = ['black','blue','brown','gray','green','orange','pink','purple','red','white','yellow']
dre_label = ['simmple','casual','dress']
vol_label = ['hikaeme','hade']

with open('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/zozotown_huku.csv','r') as rf:
    with open('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/zozotown_huku_tagadd.csv','w') as wf:
        r = csv.reader(rf)
        w = csv.writer(wf)
        cate_list=[]
        for idx,line in enumerate(r):
            if cate_list.count(line[1]) < 10:
                cate_list.append(line[1])
            else:
                continue
            print(idx)

            url = line[4]
            filename = 'sample_image.png'
            response = requests.get(url)
            dl_image = response.content
            with open('/Users/kakizakikazuki/Documents/codnate_jango/tanuki/'+filename,'wb') as image:
                image.write(dl_image)
            read_image = cv2.imread(filename,1)
            if read_image is None:
                continue
            cutx = cv2.resize(read_image,(64,64))
            #画像の色をRGB形式に変更
            cutx = cv2.cvtColor(cutx,cv2.COLOR_BGR2RGB).astype(np.float32)
            #次元数を上げる
            cutx = cutx.reshape((1,)+cutx.shape)
            cutx /= 255

            #モデルに掛ける（チェック）
            pred = model_color.predict(cutx,1,0)
            label = np.argmax(pred)
            line.append(color_label[label])
            
            pred = model_dre.predict(cutx,1,0)
            line.append(int(pred[0][0]*100))
            line.append(int(pred[0][1]*100))
            line.append(int(pred[0][2]*100))

            pred = model_vol.predict(cutx,1,0)
            label = np.argmax(pred)
            line.append(vol_label[label])

            pred = model_tag.predict(cutx,1,0)
            pred_idx = np.argsort(-pred)
            
            line.append(tag_label[pred_idx[0][0]])
            line.append(tag_label[pred_idx[0][1]])
            line.append(tag_label[pred_idx[0][2]])
            line.append(tag_label[pred_idx[0][3]])

            K.clear_session()
            print(line)
            w.writerow(line)



import csv
import codecs

check_list = ['帽子','アクセサリー','ファッション雑貨','雑貨/ホビー/スポーツ',
             'スーツ/ネクタイ','財布/小物','マタニティ・ベビー','ヘアアクセサリー',
             'ボディ・ヘアケア/コンタクト','インテリア','音楽/本・雑誌','食器/キッチン','水着/着物・浴衣','その他']

with codecs.open('zozotown.csv','r','utf-8','ignore') as f:
    with open('zozotown_huku.csv','w') as wf:
        r = csv.reader(f)
        w = csv.writer(wf)
        for row in r:
            if row[1] not in check_list :
                w.writerow(row)
                print(row)
                break

            break
            
                

    


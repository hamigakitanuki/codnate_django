from django.urls import path
from . import views

urlpatterns = [
     path(r'index',views.index,name = 'index'),
     path(r'imgInDB',views.imgInDB,name = 'imgInDB'),
     path(r'getImage',views.getImage,name = 'getImage'),
     path(r'newAccount',views.newAccount,name = 'newAccount'),
     path(r'getCodenate',views.getCodenate,name = 'getCodenate'),
     path(r'img_Delete',views.img_delete,name = 'img_Delete'),
     path(r'get_Cate',views.getCate,name = 'get_Cate'),
     path(r'get_Type',views.get_type,name = 'get_type'),
     path(r'get_Tag',views.get_tag,name = 'get_tag'),
     path(r'get_Vol',views.get_vol,name = 'get_vol'),
     path(r'get_subCate',views.getsubCate,name = 'get_subCate'),
     path(r'get_Color',views.getColor,name = 'get_subColor'),
     path(r'get_photo_count',views.get_photo_count,name = 'get_photo_count'),
     path(r'bad_codnate_post',views.bad_codnate_post,name = 'bad_codnate_post'),
     path(r'good_codnate_post',views.good_codnate_post,name = 'good_codnate_post'),
     path(r'bad_codnate_delete',views.bad_codnate_delete,name = 'bad_codnate_delete'),
     path(r'getAccount',views.getAccount,name = 'getAccount'),
     path(r'changeAccount',views.changeAccount,name = 'changeAccount'),
     path(r'get_recomend_web_item_tops',views.get_recomend_web_item_tops,name = 'get_recomend_web_item_tops'),
     path(r'get_recomend_web_item_botoms',views.get_recomend_web_item_botoms,name = 'get_recomend_web_item_botoms'),
     path(r'get_recomend_web_item_shoese',views.get_recomend_web_item_shoese,name = 'get_recomend_web_item_shoese'),
     path(r'get_recomend_list',views.get_recomend_item_list,name='get_recomend_item_list'),
     path(r'get_recomend_local_item',views.get_recomend_local_item,name = 'get_recomend_local_item'),
     path(r'post_shop_info',views.post_shop_info ,name = 'post_shop_info'),



     

]

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
     path(r'get_Casual',views.get_casual,name = 'get_casual'),
     path(r'get_Tag',views.get_tag,name = 'get_tag'),
     path(r'get_Vol',views.get_vol,name = 'get_vol'),
     path(r'get_subCate',views.getsubCate,name = 'get_subCate'),
     path(r'get_Color',views.getColor,name = 'get_subColor'),

]

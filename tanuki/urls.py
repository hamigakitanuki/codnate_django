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
]

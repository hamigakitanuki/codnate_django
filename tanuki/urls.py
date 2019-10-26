from django.urls import path
from . import views

urlpatterns = [
     path(r'index',views.index,name = 'index'),
     path(r'imgInDB',views.imgInDB,name = 'imgInDB'),
     path(r'getImage',views.getImage,name = 'getImage'),
]

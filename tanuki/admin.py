from django.contrib import admin
from .models import Photo,Account,BlackList,Sub_type_value,Color_type_value,Codnate,Photo_one

# Register your models here.
admin.site.register(Photo)
admin.site.register(Account)
admin.site.register(BlackList)
admin.site.register(Codnate)
admin.site.register(Sub_type_value)
admin.site.register(Color_type_value)
admin.site.register(Photo_one)

from django.contrib import admin
from .models import Photo,Account,BlackList

# Register your models here.
admin.site.register(Photo)
admin.site.register(Account)
admin.site.register(BlackList)

from django import forms
class PhotoForm(forms.Form):
    image = forms.ImageField()
    cate = forms.CharField(max_length=30, required=False)
    sub = forms.CharField(max_length=30, required=False)
    color = forms.CharField(max_length=30, required=False)
class AccountForm(forms.Form):
    name = forms.CharField(max_length=100)
    sex  = forms.CharField(max_length=5)
    age  = forms.IntegerField()
    type = forms.CharField(max_length=30)


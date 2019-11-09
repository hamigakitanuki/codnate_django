from django import forms
class PhotoForm(forms.Form):
    image = forms.ImageField()

class AccountForm(forms.Form):
    name = forms.CharField(max_length=100)
    sex  = forms.CharField(max_length=2)
    age  = forms.IntegerField()
    type = forms.CharField(max_length=30)


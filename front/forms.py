from django import forms

class LoginRegForm(forms.Form):
    login = forms.CharField(min_length=5)
    pas = forms.CharField(max_length=32, widget=forms.PasswordInput)

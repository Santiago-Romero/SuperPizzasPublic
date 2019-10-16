from django import forms
from .models import *


class UsuarioForm(forms.ModelForm):    
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {'password': forms.PasswordInput(),
                    'rol': forms.HiddenInput(),}
    
class LoginForm(forms.Form):
    nickname=forms.CharField(max_length=50,label="nickname")
    password=forms.CharField(max_length=75,label="password",widget=forms.PasswordInput)
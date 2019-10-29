from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UsuarioForm(forms.ModelForm):    
    class Meta:
        model = Usuario

        fields = [
        'cc',
        'telefono',
        'pais',
        'nombre_banco',
        'fecha_vencimiento',
        'tipo_tarjeta',
        'numero_tarjeta',
        'cvv'
        ]

        widgets = {'rol': forms.HiddenInput(),}

class UserForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]

        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Email',
            'username':'Nombre de Usuario',
            'password1':'Contrasena',
            'password2':'Confirmacion de Contrasena',
        }

        
        widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-label required'}),
			'email':forms.TextInput(attrs={'class':'form-label required', 'type':'email'}),
			'username':forms.TextInput(attrs={'class':'form-label required'}),
			'password1':forms.TextInput(attrs={'class':'form-label required','type':'password'}),
            'password2':forms.TextInput(attrs={'class':'form-label required','type':'password'}),
		}
    
class LoginForm(forms.Form):
    nickname=forms.CharField(max_length=50,label="nickname")
    password=forms.CharField(max_length=75,label="password",widget=forms.PasswordInput)    
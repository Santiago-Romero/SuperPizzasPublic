from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


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
        'cvv',
        'user'
        ]

        widgets = {'rol': forms.HiddenInput(),'user': forms.HiddenInput(),}

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
    
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-md','name':'username_login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-md'}))

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
        'rol',
        'user'
        ]

        widgets = {'rol': forms.HiddenInput(),'user': forms.HiddenInput(),}

class UsuarioForm2(forms.ModelForm):    
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
        'rol',
        'user'
        ]

        widgets = {'user': forms.HiddenInput(),}

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
            'first_name':forms.TextInput(attrs={'class':'form-label required form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-label required form-control'}),
            'email':forms.TextInput(attrs={'class':'form-label required form-control', 'type':'email'}),
            'username':forms.TextInput(attrs={'class':'form-label form-control required',}),
            'password1':forms.TextInput(attrs={'class':'form-label required form-control','type':'password',}),
            'password2':forms.TextInput(attrs={'class':'form-label required form-control','type':'password',}),
        }

class UpdateUser(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-label required form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-label required form-control'}),
            'email':forms.TextInput(attrs={'class':'form-label required form-control', 'type':'email'}),
        }
    
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-md','name':'username_login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-md'}))

from django import forms
from .models import *
from apps.ingredientes.models import Ingrediente


class ProductoForm(forms.ModelForm):
    ingrediente = forms.ModelMultipleChoiceField(queryset=Ingrediente.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    class Meta:
        model = Producto
        fields = ('nombre','ingrediente','valor')

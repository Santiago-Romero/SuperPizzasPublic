from django import forms
from .models import *
from apps.ingredientes.models import Ingrediente



class PizzaForm(forms.ModelForm):
    ingrediente = forms.ModelMultipleChoiceField(queryset=Ingrediente.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    class Meta:
        model = Pizza
        fields = ('nombre','ingrediente','valor','descripcion','especial','enventa')


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
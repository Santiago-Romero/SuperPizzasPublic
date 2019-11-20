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


class FacturaEstadoForm(forms.ModelForm):
    class Meta:
        model = Factura

        estado_factura_choices = (
            ('', 'Estado del pedido'),
            (1, 'En Preparación'),
            (2, 'Enviado'),
            (3, 'Cancelado'),
            (4, 'Entregado'),
        )

        fields = [
            'estado_Factura',
        ]
        labels = {
            'estado_Factura': 'Estado del pedido',
        }
        widgets = {
            'estado_Factura': forms.Select(choices=estado_factura_choices),
        }
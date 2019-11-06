from django import forms
from .models import *
from captcha.fields import ReCaptchaField


class FranquiciaForm(forms.ModelForm):
    captcha = ReCaptchaField(label="Debe realizar la verificación captcha.")
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        super(FranquiciaForm, self).__init__(*args, **kwargs)
        self.fields['schema_name'].label = "Subdominio "
        self.fields['schema_name'].help_text = "Esta será su direccion: midireccion%s" % settings.DOMAIN
        # self.fields['tipo'].widget.attrs['disabled'] = 'disabled'
       

    class Meta:
        model = Franquicia
        fields = ('nombre', 'schema_name','tipo')
        
  
                
    def clean_schema_name(self):
        direccion_tenant = self.cleaned_data["schema_name"]
        if direccion_tenant.lower() == 'www':
            self.add_error("schema_name", "No es posible registrar %s como dirección en el sistema" % direccion_tenant)

        return direccion_tenant


class ModificarFranquiciaForm(forms.ModelForm):
    class Meta:
        model = Franquicia
        fields = ('nombre', 'tipo')
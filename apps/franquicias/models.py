from django.db import models
import datetime
from django_tenants.models import TenantMixin, DomainMixin
## from colorfield.fields import ColorField
## para el color pip install django-colorfield

class TipoFranquicia(models.Model):
    nombre = models.CharField(max_length=100)  
    precio= models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Franquicia(TenantMixin):
    nombre = models.CharField(max_length=50)    
    fecha_corte =  models.DateField(auto_now_add=True)
    tipo = models.ForeignKey(TipoFranquicia,default=None, on_delete=models.CASCADE)
    configuracion  = models.CharField(max_length=200, default='{"colorprimario":"#1D1D1D","colorsecundario":"#E9951F", "tamanioletra":100}')
    media = models.FileField(upload_to='media/logos-franquicias/', default='media/logos-franquicias/1_logo_default.png', blank=True, null=True)
    ##imagen = models.ImageField(upload_to = 'static/landingpage/images', default = 'static/landingpage/images/logo.png')
    ##primario = ColorField(default='#FF0000')
    ##secundario = ColorField(default='#FF0000').
    working=models.BooleanField(default=True)
    auto_create_schema = True

    def __str__(self):
        return self.nombre
    
   

class Dominio(DomainMixin):
    pass


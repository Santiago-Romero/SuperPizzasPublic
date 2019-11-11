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
    imagen = models.ImageField(upload_to = 'images', default = 'logo.png')
    ##primario = ColorField(default='#FF0000')
    ##secundario = ColorField(default='#FF0000').
    working=models.BooleanField(default=True)
    auto_create_schema = True

    def __str__(self):
        return self.nombre

class Dominio(DomainMixin):
    pass


from django.db import models
import datetime
from django_tenants.models import TenantMixin, DomainMixin

class TipoFranquicia(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Franquicia(TenantMixin):
    nombre = models.CharField(max_length=100)
    fecha_corte =  models.DateField(auto_now_add=True)
    tipo = models.ForeignKey(TipoFranquicia,default=None, on_delete=models.CASCADE)
    auto_create_schema = True

    def __str__(self):
        return self.nombre

class Dominio(DomainMixin):
    pass


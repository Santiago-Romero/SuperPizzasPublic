from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Franquicia(TenantMixin):
    id = models.AutoField
    nombre = models.CharField(max_length=100)
    fecha_corte =  models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.nombre

class Dominio(DomainMixin):
    pass
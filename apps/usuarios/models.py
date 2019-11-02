from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Roles = (('d', 'Digitador'), ('v', 'Vendedor'), ('a', 'Admin'))     
    cc=models.BigIntegerField()
    telefono= models.BigIntegerField()
    pais=models.CharField(max_length=50)
    nombre_banco=models.CharField(max_length=50)
    fecha_vencimiento=models.DateField(default=timezone.now)
    tipo_tarjeta=models.CharField(max_length=50)
    numero_tarjeta=models.BigIntegerField()
    cvv=models.IntegerField()
    rol=models.CharField(max_length=1, choices=Roles)
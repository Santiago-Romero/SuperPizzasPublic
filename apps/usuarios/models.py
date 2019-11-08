from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Roles = (('d', 'Digitador'), ('v', 'Vendedor'), ('a', 'Admin'), ('c', 'Cliente'))     
    cc=models.BigIntegerField(default=1234567890)
    telefono= models.BigIntegerField(default=1234567890)
    pais=models.CharField(max_length=50,default="Colombia")
    nombre_banco=models.CharField(max_length=50,default="Davivienda")
    fecha_vencimiento=models.DateField(default=timezone.now)
    tipo_tarjeta=models.CharField(max_length=50,default="Visa")
    numero_tarjeta=models.BigIntegerField(default=123456789012345)
    cvv=models.IntegerField(default=123)
    rol=models.CharField(max_length=1, choices=Roles)
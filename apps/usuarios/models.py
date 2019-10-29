from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Roles = (('d', 'Digitador'), ('v', 'Vendedor'), ('a', 'Admin'))     
    cc=models.BigIntegerField(default=1115087926)
    telefono= models.BigIntegerField(default=3154879521)
    pais=models.CharField(max_length=50,default='Colombia')
    nombre_banco=models.CharField(max_length=50,default="bancolombia")
    fecha_vencimiento=models.DateField(default=timezone.now)
    tipo_tarjeta=models.CharField(max_length=50,default="master card")
    numero_tarjeta=models.IntegerField(default=1546543214)
    cvv=models.IntegerField(default=4562)
    rol=models.CharField(max_length=1, choices=Roles)
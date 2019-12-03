from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Roles = (('d', 'Digitador'), ('v', 'Vendedor'), ('a', 'Admin'), ('c', 'Cliente'))
    tiposTarjetas=(('visa', 'Visa'), ('master', 'Master Card'))
    bancos=(('bancolombia', 'Bancolombia'), ('davivienda', 'Davivienda'), ('bogota', 'Banco de Bogotá'), ('bbva', 'BBVA'))
    cc=models.BigIntegerField()
    telefono= models.BigIntegerField()
    nombre_banco=models.CharField(max_length=50,choices=bancos,default='bancolombia')
    fecha_vencimiento=models.DateField(default=timezone.now)
    tipo_tarjeta=models.CharField(max_length=50,choices=tiposTarjetas,default='visa')
    numero_tarjeta=models.BigIntegerField()
    cvv=models.IntegerField()
    direccion=models.CharField(max_length=200, blank=True,null=True)
    rol=models.CharField(max_length=1, choices=Roles)
    fecha_creacion = models.DateField(auto_now_add=True)
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Roles = (('d', 'Digitador'), ('v', 'Vendedor'), ('a', 'Admin'), ('c', 'Cliente'))
    tiposTarjetas=(('visa', 'Visa'), ('master', 'Master Card'))
    bancos=(('bancolombia', 'Bancolombia'), ('davivienda', 'Davivienda'), ('bogota', 'Banco de Bogotá'), ('bbva', 'BBVA'))
    cc=models.BigIntegerField(default=1234567890)
    telefono= models.BigIntegerField(default=1234567890)
    pais=CountryField(default='CO')
    nombre_banco=models.CharField(max_length=50,choices=bancos,default='bancolombia')
    fecha_vencimiento=models.DateField(default=timezone.now)
    tipo_tarjeta=models.CharField(max_length=50,choices=tiposTarjetas,default='visa')
    numero_tarjeta=models.BigIntegerField(default=123456789012345)
    cvv=models.IntegerField(default=123)
    direccion=models.TextField(default='calle 13a 5e-01 Buga', blank=True,null=True)
    rol=models.CharField(max_length=1, choices=Roles)
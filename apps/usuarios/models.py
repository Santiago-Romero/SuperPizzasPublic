from django.db import models
import datetime

class Roles(models.Model):
    nombre=models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Usuario(models.Model):        
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    cc=models.BigIntegerField(default=1115087926)
    telefono= models.IntegerField(default=3154879521)
    email=models.EmailField(default="null@gmail.com")
    pais=models.CharField(max_length=50,default='Colombia')
    nickname=models.CharField(max_length=12)
    password=models.CharField(max_length=12)
    nombre_banco=models.CharField(max_length=50,default="bancolombia")
    fecha_vencimiento=models.DateField(auto_now=True)
    tipo_tarjeta=models.CharField(max_length=50,default="master card")
    numero_tarjeta=models.IntegerField(default=1546543214)
    cvv=models.IntegerField(default=4562)

    


    rol=models.ForeignKey(Roles,default=None, on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname


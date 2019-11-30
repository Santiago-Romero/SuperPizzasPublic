from django.db import models
from apps.ingredientes.models import Ingrediente


class Pizza(models.Model):
    nombre = models.CharField(max_length=50)
    ingrediente = models.ManyToManyField('ingredientes.Ingrediente')
    valor = models.BigIntegerField()
    descripcion = models.CharField(max_length=250,default="")
    especial =  models.BooleanField(default=True)
    enventa = models.BooleanField(default=True)
    imagen = models.FileField(upload_to='media/pizzas/', blank=True, null=True)
    def __str__(self):
        return self.nombre

class Factura(models.Model):    
    cliente = models.ForeignKey('usuarios.usuario', on_delete=models.CASCADE)
    ciudad= models.CharField(max_length=80)
    direccion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    hora_creacion = models.TimeField(auto_now_add=True)
   

class Detalle(models.Model):
    factura = models.ForeignKey(Factura,on_delete=models.CASCADE)
    producto = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.FloatField()

class IngredientesA(models.Model):
    factura=models.ForeignKey(Factura,on_delete=models.CASCADE,default=1)
    producto=models.ForeignKey(Pizza,on_delete=models.CASCADE,default=1)
    ingredientes= models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.FloatField()

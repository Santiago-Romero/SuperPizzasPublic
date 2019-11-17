from django.db import models


class Pizza(models.Model):
    nombre = models.CharField(max_length=50)
    ingrediente = models.ManyToManyField('ingredientes.Ingrediente')
    valor = models.BigIntegerField()
    descripcion = models.CharField(max_length=250,default="")
    especial =  models.BooleanField(default=True)
    enventa = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Factura(models.Model):    
    cliente = models.ForeignKey('usuarios.usuario', on_delete=models.CASCADE)
    direccion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    hora_creacion = models.TimeField(auto_now_add=True)
    efectivo = models.FloatField(default=0)
    estado_Factura = models.IntegerField(default=0)


class Detalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.FloatField()


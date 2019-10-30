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

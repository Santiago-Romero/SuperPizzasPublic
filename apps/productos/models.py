from django.db import models

class Producto(models.Model):
    #id = models.AutoField
    nombre = models.CharField(max_length=100)
    valor = models.BigIntegerField()
    def __str__(self):
        return self.nombre

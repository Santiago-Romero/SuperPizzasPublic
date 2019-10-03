from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.BigIntegerField()
    def __str__(self):
        return self.nombre

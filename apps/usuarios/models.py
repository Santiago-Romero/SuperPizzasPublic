from django.db import models

class Roles(models.Model):
    nombre=models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nickname=models.CharField(max_length=12)
    password=models.CharField(max_length=12)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    rol=models.ForeignKey(Roles,default=None, on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname


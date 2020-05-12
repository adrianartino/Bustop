from django.db import models

# Create your models here.
class Usuarios(models.Model):
    usuario = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    contrasena = models.CharField(max_length=30)
    localidad = models.CharField(max_length=30)
    correo = models.CharField(max_length=30)
    nacimiento = models.DateField()


class Rutas(models.Model):
    nombre_ruta = models.CharField(max_length=20, primary_key=True)
    ncamiones = models.IntegerField()
    color = models.CharField(max_length=30)
    tiempo = models.IntegerField()

class Admin(models.Model):
    nombre_admin = models.CharField(max_length=20, primary_key=True)
    contrasena = models.CharField(max_length=30)
    correo = models.CharField(max_length=30)


class Concesionario(models.Model):
    conce = models.CharField(max_length=20, primary_key=True)
    contrasena = models.CharField(max_length=30)
    nombre_conce = models.CharField(max_length=30)
    nombre_ruta = models.CharField(max_length=20)
    correo = models.CharField(max_length=30)


class rutasBuscadas(models.Model):
    usuario = models.CharField(max_length=20)
    nombre_ruta = models.CharField(max_length=20)


class rutasAgregadas(models.Model):
    nombre_ruta = models.CharField(max_length=20)
    nombre_admin = models.CharField(max_length=20)


class ConcAgregados(models.Model):
    conce = models.CharField(max_length=20)
    nombre_admin = models.CharField(max_length=20)


class QuejasUsuarios(models.Model):
    usuario = models.CharField(max_length=20)
    nombre_ruta = models.CharField(max_length=20)
    fecha = models.DateField()
    texto = models.TextField()


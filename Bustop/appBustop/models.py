from django.db import models

# Create your models here.
class Usuarios(models.Model):
    usuario = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    nacimiento = models.DateField()


class Rutas(models.Model):
    nombre_ruta = models.CharField(max_length=255, primary_key=True)
    localidad = models.CharField(max_length=255)
    ncamiones = models.IntegerField()
    color = models.CharField(max_length=255)
    tiempo = models.IntegerField()

class Admin(models.Model):
    nombre_admin = models.CharField(max_length=255, primary_key=True)
    contrasena = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)


class Concesionario(models.Model):
    conce = models.CharField(max_length=255, primary_key=True)
    contrasena = models.CharField(max_length=255)
    nombre_conce = models.CharField(max_length=255)
    nombre_ruta = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)


class rutasBuscadas(models.Model):
    usuario = models.CharField(max_length=255)
    nombre_ruta = models.CharField(max_length=255)


class rutasAgregadas(models.Model):
    nombre_ruta = models.CharField(max_length=255)
    nombre_admin = models.CharField(max_length=255)


class ConcAgregados(models.Model):
    conce = models.CharField(max_length=255)
    nombre_admin = models.CharField(max_length=255)


class QuejasUsuarios(models.Model):
    usuario = models.CharField(max_length=255, primary_key=True)
    unidad = models.IntegerField()
    nombre_ruta = models.CharField(max_length=255)
    fecha = models.DateField()
    texto = models.TextField()


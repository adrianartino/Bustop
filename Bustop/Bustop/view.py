from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render


#LOGIN
def login(request):

    return render(request, "Principal/login.html")

def registro(request):

    return render(request, "Principal/registro.html")


def olvido(request):

    return render(request, "Principal/olvidoContra.html")

#USUARIOS PRINCIPAL
def principalUsuario(request):

    return render(request, "Usuarios/bienUsuario.html")

#BUSCAR RUTA
def buscarRuta(request):

   return render(request, "Usuarios/bRutaUsuario.html")

#BUSCAR RUTA POS UBICACIÓN.
def ubicacionRuta(request):

   return render(request, "Usuarios/ubiUsuario.html")

#MAPAS
def mapaRutaTorreon(request):

   return render(request, "Usuarios/Mapas/mapaTorreon.html")


def mapaRutaGomez(request):

   return render(request, "Usuarios/Mapas/mapaGomez.html")


def mapaRutaLerdo(request):

   return render(request, "Usuarios/Mapas/mapaLerdo.html")

#QUEJAS Y SUGERENCIAS.
def quejaUsuario(request):

   return render(request, "Usuarios/quejaUsuario.html")


#CONSESIONARIOS ----------------------------------------------------------------------------------------------
def principalCons(request):

   return render(request, "Consesionario/bienCons.html")

def infoCons(request):

   return render(request, "Consesionario/infoCons.html")

def quejasCons(request):

   return render(request, "Consesionario/quejasCons.html")

def usuariosCons(request):

   return render(request, "Consesionario/usuariosCons.html")


#ADMINISTRADORES ----------------------------------------------------------------------------------------------
def principalAdmin(request):

   return render(request, "Administrador/bienAdmin.html")

def altaRuta(request):

   return render(request, "Administrador/altaRuta.html")

def altaCons(request):

   return render(request, "Administrador/altaCons.html")


#ACTUALIZAR DATOS ----------------------------------------------------------------------------------------------
def actUsuario(request):

   return render(request, "Actualizar/actUsuario.html")

def actCons(request):

   return render(request, "Actualizar/actCons.html")


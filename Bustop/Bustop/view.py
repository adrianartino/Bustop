from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render

def prueba(request):

    persona = "Gabriel es puto"

    return render(request, "Principal/padrePrincipal.html", {"variable": persona})

#LOGIN
def login(request):

    persona = "Gabriel es puto"
    
    return render(request, "Principal/login.html", {"variable": persona})

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



from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from appBustop.models import Usuarios

# Create your views here.

#LOGIN

def login(request):

    return render(request, "Principal/login.html")


def registro(request):

   if request.method == "POST":
      
      nombreusuario = request.POST['nombreusuario']
      nombre = request.POST['nombre']
      apellido = request.POST['apellido']
      contra = request.POST['contra']
      cc = request.POST['contraconfirmada']
      localidad = request.POST['localidad']
      correo = request.POST['correo']
      nacimiento = request.POST['nacimiento']
   
      textoerror = ""
      error = False
      error2 = False
      error3 = False

      if contra == cc:
         error = False
            
      else:
         error = True
         textoerror += " Las contraseñas no coinciden. "


         
      if localidad == "l":
         error2 = True
         textoerror += " Selecciona una localidad. "
      else:
         error2 = False
         


      if nacimiento == "":
         error3 = True
         textoerror += " Falta ingresar la fecha de nacimiento. "
      else:
         error3 = False

      #si hay un error
      if error == True or error2 == True or error3 == True:
         hayerror = True
         return render(request, "Principal/registro.html", {"bandera":hayerror, "textoerror":textoerror, "nombreusuario":nombreusuario, "nombre":nombre, "apellido":apellido, "contra":contra, "cc":cc, "localidad":localidad, "correo":correo, "nacimiento":nacimiento})

         #return HttpResponse(textoerror)
      #si no hay errores
      elif error == False:
         hayerror = False

         registro = Usuarios(usuario = nombreusuario, nombre = nombre, apellido = apellido, contrasena = contra, localidad = localidad, correo = correo, nacimiento = nacimiento)
         registro.save()
         return render(request, "Principal/registro.html", {"bandera": hayerror})
         #datos = nombreusuario , " " , nombre , " " , apellido , " " , contra , " " , cc , " " , localidad , " " , correo , " " , nacimiento
         #return HttpResponse(datos)
      
   
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

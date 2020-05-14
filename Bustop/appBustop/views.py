from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import redirect

#importar lo del email
from django.conf import settings
from django.core.mail import send_mail

#importar modelos
from appBustop.models import Usuarios



# Create your views here.

#LOGIN

def login(request):

   #si hay una sesion iniciada...
   if "sesion" in request.session:
      return redirect('/principalUsuario/')
   
   else:
      if request.method == "POST":
         
         nombreusuario = request.POST['nombreusuario']
         contra = request.POST['contrausuario']

         datospersona = Usuarios.objects.filter(usuario__icontains=nombreusuario)

         #Si encuentra a una persona con ese usuario
         if datospersona :

            for dato in datospersona:
               contrareal = dato.contrasena
               nombre = dato.nombre
               apellido = dato.apellido
               localidad = dato.localidad
               correo = dato.correo
               nacimiento = dato.nacimiento
            
            #Si ingresa bien su usuario y contraseña
            if contra == contrareal:

               request.session['sesion'] = nombreusuario
               request.session['nombre'] = nombre
               request.session['apellido'] = apellido
               return redirect('/principalUsuario/')

            #Contraseña esta mal
            else:
               bandera = True
               bandera2 = True
               error = "Ha ingresado mal la contraseña."
               return render(request, "Principal/login.html", {"bandera": bandera, "bandera2": bandera2, "error": error, "nombreusuario": nombreusuario})
               # return HttpResponse(mensaje)

         #si no se encuentra a alguien con ese usuario..
         else:
            bandera = True
            error = "No se ha encontrado a nadie con ese usuario."
            return render(request, "Principal/login.html", {"bandera": bandera, "error": error})
            # mensaje = "No se encontro alguien con ese usuario xd"
            # return HttpResponse(mensaje)


      return render(request, "Principal/login.html")

def salir(request):
   del request.session["sesion"]
   del request.session['nombre']
   del request.session['apellido'] 

   return redirect('/login/')

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

   #si se da clic en el boton..
   if request.method == "POST":

      nombreusuario = request.POST['nombreusuario']

      datospersona = Usuarios.objects.filter(usuario__icontains=nombreusuario)

      if datospersona:

         for dato in datospersona:
            nombre = dato.nombre
            apellido = dato.apellido
            correo = dato.correo
            contraseña = dato.contrasena
         
         email_remitente = settings.EMAIL_HOST_USER
         email_destino = [correo]
         
         asunto = "Recuperación de contraseña - Bustop"
         mensaje = "Hola "+ nombre+ " "+ apellido+ ". Tu contraseña es: "+ contraseña+ "."

         send_mail(asunto, mensaje, email_remitente, ["brandonmora850@gmail.com"])

         return render(request, "Principal/olvidoContra.html", {"datospersona":datospersona,"busqueda":nombreusuario, "nombre":nombre, "apellido":apellido})

      else:
         error = "No se encontro el usuario."
         bandera = True
         return render(request, "Principal/olvidoContra.html", {"error": error, "bandera": bandera})
      #return HttpResponse(datospersona)

   
   return render(request, "Principal/olvidoContra.html")

#USUARIOS PRINCIPAL


def principalUsuario(request):

    return render(request, "Usuarios/bienUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})

#BUSCAR RUTA


def buscarRuta(request):

   return render(request, "Usuarios/bRutaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})

#BUSCAR RUTA POS UBICACIÓN.


def ubicacionRuta(request):

   return render(request, "Usuarios/ubiUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})

#MAPAS


def mapaRutaTorreon(request):

   return render(request, "Usuarios/Mapas/mapaTorreon.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})


def mapaRutaGomez(request):

   return render(request, "Usuarios/Mapas/mapaGomez.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})


def mapaRutaLerdo(request):

   return render(request, "Usuarios/Mapas/mapaLerdo.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})

#QUEJAS Y SUGERENCIAS.


def quejaUsuario(request):

   return render(request, "Usuarios/quejaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})


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

   return render(request, "Actualizar/actUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido']})


def actCons(request):

   return render(request, "Actualizar/actCons.html")

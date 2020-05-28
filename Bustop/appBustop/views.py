from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import redirect

#importar lo del email
from django.conf import settings
from django.core.mail import send_mail

#importar modelos
from appBustop.models import Usuarios, Rutas, QuejasUsuarios, Admin, Concesionario, rutasAgregadas, ConcAgregados, rutasBuscadas

from datetime import datetime

from django.contrib.postgres.search import SearchQuery, SearchVector

usuarioNormalLoguqado = False
adminLogueado = False
consLogueado = False

# Create your views here.

#LOGIN

def login(request):

   #si hay una sesion iniciada...
   if "sesion" in request.session:
      return redirect('/principalUsuario/')
   
   elif "admin" in request.session:
      return redirect('/principalAdmin/')
   
   elif "conce" in request.session:
      return redirect('/principalCons/')
   
   else:
      if request.method == "POST":
         
         nombreusuario = request.POST['nombreusuario']
         contra = request.POST['contrausuario']

         datospersona = Usuarios.objects.filter(usuario__icontains=nombreusuario)

         administradores = Admin.objects.filter(
             nombre_admin__icontains=nombreusuario)

         concesionarios = Concesionario.objects.filter(
             conce__icontains=nombreusuario)

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

               usuarioNormalLoguqado = True

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

         #si se encuentra en administradores.
         elif administradores:

            for dato in administradores:
               contrareal = dato.contrasena
               correo = dato.correo

            #Si ingresa bien su usuario y contraseña
            if contra == contrareal:

               request.session['admin'] = nombreusuario
               return redirect('/principalAdmin/')

            #Contraseña esta mal
            else:
               bandera = True
               bandera2 = True
               error = "Ha ingresado mal la contraseña."
               return render(request, "Principal/login.html", {"bandera": bandera, "bandera2": bandera2, "error": error, "nombreusuario": nombreusuario})
               # return HttpResponse(mensaje)

         elif concesionarios:

            for dato in concesionarios:
               contrareal = dato.contrasena
               nombre = dato.nombre_conce
               rutaencargado = dato.nombre_ruta
               correo = dato.correo

            #Si ingresa bien su usuario y contraseña
            if contra == contrareal:

               request.session['conce'] = nombreusuario
               request.session['nombreconce'] = nombre
               return redirect('/principalCons/')

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


def salirAdmin(request):
   del request.session["admin"]

   return redirect('/login/')


def salirCons(request):
   del request.session["conce"]
   del request.session['nombreconce']

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

      usuariosregistrados = Usuarios.objects.all()

      for u in usuariosregistrados:
         #si el nombre ingresado es igual a un usuario ya registrado...

         if nombreusuario == u.usuario:
            error = "Ya hay un usuario registrado con ese nombre."
            hayerror = True
            return render(request, "Principal/registro.html", {"bandera": hayerror, "textoerror": error, "nombreusuario": nombreusuario, "nombre": nombre, "apellido": apellido, "contra": contra, "cc": cc, "localidad": localidad, "correo": correo, "nacimiento": nacimiento})

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
         return render(request, "Principal/registro.html", {"bandera": hayerror, "textoerror": textoerror, "nombreusuario": nombreusuario, "nombre": nombre, "apellido":apellido, "contra":contra, "cc":cc, "localidad":localidad, "correo":correo, "nacimiento":nacimiento})

            #return HttpResponse(textoerror)
      #si no hay errores
      elif error == False:
         hayerror = False

         registro = Usuarios(usuario=nombreusuario, nombre=nombre, apellido = apellido, contrasena = contra, localidad = localidad, correo = correo, nacimiento = nacimiento)
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
         mensaje = "Hola "+ nombre+ " "+ apellido+ "!. Creemos que olvidaste tu contraseña :(. Tu contraseña es: "+ contraseña+ "."

         send_mail(asunto, mensaje, email_remitente, email_destino)

         return render(request, "Principal/olvidoContra.html", {"datospersona":datospersona,"busqueda":nombreusuario, "nombre":nombre, "apellido":apellido})

      else:
         error = "No se encontro el usuario."
         bandera = True
         return render(request, "Principal/olvidoContra.html", {"error": error, "bandera": bandera})
      #return HttpResponse(datospersona)

   
   return render(request, "Principal/olvidoContra.html")

#USUARIOS PRINCIPAL


def principalUsuario(request):

   principal = True

   return render(request, "Usuarios/bienUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "principal":principal})

   

#BUSCAR RUTA


def buscarRuta(request):
   buscarin = True
   #cuando el usuario de clic en buscar..
   if request.method == "POST":

      busqueda = request.POST['busqueda']
      buscarin = True


      #Si funciona pero con la búsqueda exacta
      busquedaRutas = Rutas.objects.annotate(
          search=SearchVector('nombre_ruta', 'color', 'localidad')
      ).filter(search=SearchQuery(busqueda))
      #busquedaRutas = Rutas.objects.annotate(search=SearchVector('nombre_ruta', 'localidad', 'color'),).filter(search=busqueda)

      #si encuentra algo relacionado con esa búsqueda..
      if busquedaRutas:
         encontro = True
         return render(request, "Usuarios/bRutaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "busquedaRutas":busquedaRutas, "encontro":encontro, "busqueda":busqueda, "buscarin":buscarin})
      
      #si no hay resultados..
      noencontro = True
      return render(request, "Usuarios/bRutaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "noencontro": noencontro, "busqueda": busqueda, "buscarin": buscarin})

   return render(request, "Usuarios/bRutaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "buscarin": buscarin})

def infoRuta(request):

   #se obtiene el nombre de la ruta de la cual el usuario quiere info 
   nombreRuta = request.POST['nomreRuta']

   rutaBuscada = rutasBuscadas(usuario=request.session['sesion'], nombre_ruta = nombreRuta)
   rutaBuscada.save()

   infoRuta = Rutas.objects.filter(nombre_ruta__icontains=nombreRuta)

   for x in infoRuta:
      localidad = x.localidad
      ncamiones = x.ncamiones
      color = x.color
      tiempo = x.tiempo

   return render(request, "Usuarios/infoRuta.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'] , "nombreRuta":nombreRuta, "localidad":localidad, "ncamiones":ncamiones, "color":color, "tiempo":tiempo})

#BUSCAR RUTA POS UBICACIÓN.


def ubicacionRuta(request):

   buscarubi = True
   return render(request, "Usuarios/ubiUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "buscarubi": buscarubi})

#MAPAS


def mapaRutaTorreon(request):

   rutasTorreon = Rutas.objects.filter(localidad__icontains="Torreon")

   return render(request, "Usuarios/Mapas/mapaTorreon.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "rutasTorreon":rutasTorreon})


def mapaRutaGomez(request):

   rutasGomez = Rutas.objects.filter(localidad__icontains="Gomez Palacio")

   return render(request, "Usuarios/Mapas/mapaGomez.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "rutasGomez": rutasGomez})


def mapaRutaLerdo(request):

   rutasLerdo = Rutas.objects.filter(localidad__icontains="Lerdo")

   return render(request, "Usuarios/Mapas/mapaLerdo.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "rutasLerdo": rutasLerdo})

#QUEJAS Y SUGERENCIAS.


def quejaUsuario(request):

   quejita = True

   rutasGomez = Rutas.objects.filter(localidad="Gomez Palacio")
   rutasLerdo = Rutas.objects.filter(localidad="Lerdo")
   rutasTorreon = Rutas.objects.filter(localidad__icontains="Torreon")

   #si se da clic en el boton..
   if request.method == "POST":
      quejita = True
      ruta = request.POST['ruta']
      unidad = request.POST['unidad']
      texto = request.POST['texto']

      fecha = datetime.now()

      if ruta == "l":
         bandera=True
         return render(request, "Usuarios/quejaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "arregloTorreon": rutasTorreon, "arregloGomez": rutasGomez, "arregloLerdo": rutasLerdo, "bandera":bandera, "unidad":unidad, "texto2":texto, "quejita":quejita})

      registroQueja = QuejasUsuarios(usuario=request.session['sesion'], nombre_ruta=ruta, unidad=unidad, fecha=fecha, texto=texto)
      registroQueja.save()

      bandera2 = True
      
      return render(request, "Usuarios/quejaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "arregloTorreon": rutasTorreon, "arregloGomez": rutasGomez, "arregloLerdo": rutasLerdo, "bandera2": bandera2, "quejita": quejita})
   
   return render(request, "Usuarios/quejaUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "arregloTorreon": rutasTorreon, "arregloGomez": rutasGomez, "arregloLerdo": rutasLerdo, "quejita": quejita})


#CONSESIONARIOS ----------------------------------------------------------------------------------------------
def principalCons(request):
   principal = True
   return render(request, "Consesionario/bienCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "principal": principal})


def infoCons(request):

   infu = True
   infoCon = Concesionario.objects.filter(conce=request.session['conce'])

   for i in infoCon:
      rutaEncargada = i.nombre_ruta

   infoRuta = Rutas.objects.filter(nombre_ruta = rutaEncargada)

   return render(request, "Consesionario/infoCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "infoRuta": infoRuta, "infu":infu})


def quejasCons(request):

   queco = True

   infoCon = Concesionario.objects.filter(conce=request.session['conce'])

   for i in infoCon:
      rutaEncargada = i.nombre_ruta

   quejas = QuejasUsuarios.objects.filter(nombre_ruta=rutaEncargada)

   contador = 0

   for i in quejas:
      contador += 1
   return render(request, "Consesionario/quejasCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "rutaEncargada": rutaEncargada, "contador": contador, "queco":queco})



def usuariosCons(request):

   usuco = True
   infoCon = Concesionario.objects.filter(conce=request.session['conce'])

   for i in infoCon:
      rutaEncargada = i.nombre_ruta

   busquedas = rutasBuscadas.objects.filter(nombre_ruta=rutaEncargada)

   contador = 0

   for i in busquedas:
      contador += 1

   return render(request, "Consesionario/usuariosCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "rutaEncargada": rutaEncargada, "contador": contador, "usuco":usuco})


#ADMINISTRADORES ----------------------------------------------------------------------------------------------
def principalAdmin(request):

   principal = True

   return render(request, "Administrador/bienAdmin.html", {"nombreusuario": request.session['admin'], "principal":principal})


def altaRuta(request):

   alru = True
   if request.method == "POST":

      alru = True
      nombreRuta = request.POST['nombreRuta']
      numeroCamiones = request.POST['numeroCamiones']
      localidad = request.POST['localidad']
      minutos = request.POST['minutos']

      color = ""

      todasRutas = Rutas.objects.all()

      for u in todasRutas:

         if nombreRuta == u.nombre_ruta:
            bandera = True
            error = "Ya existe esa ruta."
            return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "textoerror": error, "bandera": bandera, "nombreRuta": nombreRuta, "numeroCamiones": numeroCamiones, "localidad":localidad, "minutos":minutos, "alru":alru})
      

      if localidad == "l":
         error = "No se ha escogido la localidad de la ruta."
         bandera = True
         return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "textoerror": error, "bandera": bandera, "nombreRuta": nombreRuta, "numeroCamiones": numeroCamiones, "localidad": localidad, "minutos": minutos, "alru": alru})
      
      if minutos == "":
         error = "Tiempo aproximado no valido."
         bandera = True
         return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "textoerror": error, "bandera": bandera, "nombreRuta": nombreRuta, "numeroCamiones": numeroCamiones, "localidad": localidad, "minutos": minutos, "alru": alru})
      
      if minutos != "":
         minutos2 = int(minutos)

         if minutos2 < 5:
            error = "Tiempo aproximado no valido."
            bandera = True
            return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "textoerror": error, "bandera": bandera, "nombreRuta": nombreRuta, "numeroCamiones": numeroCamiones, "localidad": localidad, "minutos": minutos, "alru": alru})

      if localidad == "Torreon":
         color = "Verde"

      if localidad == "Gomez Palacio":
         color = "Azul"

      if localidad == "Lerdo":
         color = "Rojo"

      bandera2 = True
      registroRuta = Rutas(nombre_ruta=nombreRuta, localidad=localidad,
                           ncamiones=numeroCamiones, color=color, tiempo=minutos)
      registroRuta.save()

      registroAdmin = rutasAgregadas(
          nombre_ruta=nombreRuta, nombre_admin=request.session['admin'])
      registroAdmin.save()

      return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "bandera2": bandera2, "alru": alru})

   return render(request, "Administrador/altaRuta.html", {"nombreusuario": request.session['admin'], "alru": alru})


def altaCons(request):

   alco = True
   rutas = Rutas.objects.all()

   if request.method == "POST":

      alco = True
      usuarioCons = request.POST['usuarioCons']
      contraCons = request.POST['contraCons']
      nombreCons = request.POST['nombreCons']
      rutaCons = request.POST['rutaCons']
      correoCons = request.POST['correoCons']

      todosCons = Concesionario.objects.all()

      for u in todosCons:

         if usuarioCons == u.conce:
            bandera = True
            error = "Ya existe ese consesionario."
            return render(request, "Administrador/altaCons.html", {"nombreusuario": request.session['admin'], "textoerror": error , "rutas": rutas ,"bandera": bandera, "usuarioCons": usuarioCons, "nombreCons": nombreCons, "rutaCons": rutaCons, "correoCons": correoCons, "alco":alco})

      #si no elige ruta
      if rutaCons == "l":

         bandera = True
         return render(request, "Administrador/altaCons.html", {"nombreusuario": request.session['admin'], "rutas": rutas, "bandera": bandera, "usuarioCons": usuarioCons, "nombreCons": nombreCons, "rutaCons": rutaCons, "correoCons": correoCons, "alco": alco})

      registroCons = Concesionario(conce=usuarioCons, contrasena=contraCons, nombre_conce=nombreCons, nombre_ruta=rutaCons, correo=correoCons)
      registroCons.save()

      registroAdmin = ConcAgregados(
          conce=usuarioCons, nombre_admin=request.session['admin'])
      registroAdmin.save()

      bandera2 = True
      return render(request, "Administrador/altaCons.html", {"nombreusuario": request.session['admin'], "rutas": rutas, "bandera2": bandera2, "alco": alco})

   return render(request, "Administrador/altaCons.html", {"nombreusuario": request.session['admin'], "rutas": rutas, "alco": alco})

def bajaRuta(request):

   baru = True

   rutas = Rutas.objects.all()

   rutasAdmin = rutasAgregadas.objects.all()

   lista = zip(rutas,rutasAdmin)

   if request.method == "POST":

      baru = True

      rutaEliminar = request.POST['rutaEliminar']

      r = Rutas.objects.get(nombre_ruta = rutaEliminar)

      t = rutasAgregadas.objects.get(nombre_ruta=rutaEliminar)


      r.delete()
      t.delete()

      rutas = Rutas.objects.all()

      rutasAdmin = rutasAgregadas.objects.all()

      lista = zip(rutas, rutasAdmin)

      bandera = True

      return render(request, "Administrador/bajaRuta.html", {"nombreusuario": request.session['admin'], "rutas": rutas, "rutasAdmin": rutasAdmin, "lista": lista, "bandera": bandera, "baru":baru})

   return render(request, "Administrador/bajaRuta.html", {"nombreusuario": request.session['admin'], "rutas": rutas, "rutasAdmin": rutasAdmin, "lista": lista, "baru": baru})


def bajaCons(request):

   baco = True

   consecionarios = Concesionario.objects.all()

   consAdmin = ConcAgregados.objects.all()

   lista = zip(consecionarios, consAdmin)

   if request.method == "POST":

      baco = True

      consEliminar = request.POST['consEliminar']

      r = Concesionario.objects.get(conce=consEliminar)

      t = ConcAgregados.objects.get(conce=consEliminar)


      r.delete()
      t.delete()

      consecionarios = Concesionario.objects.all()

      consAdmin = ConcAgregados.objects.all()

      lista = zip(consecionarios, consAdmin)

      bandera = True

      return render(request, "Administrador/bajaCons.html", {"nombreusuario": request.session['admin'], "con": consecionarios, "consAdmin": consAdmin, "lista": lista, "bandera": bandera, "baco":baco})

   return render(request, "Administrador/bajaCons.html", {"nombreusuario": request.session['admin'], "lista": lista, "baco": baco})


#ACTUALIZAR DATOS ----------------------------------------------------------------------------------------------
def actUsuario(request):

   if request.method == "POST":

      actusuario = request.POST['actusuario']
      actapellido = request.POST['actapellido']
      actcontrasena = request.POST['actcontrasena']
      actlocalidad = request.POST['actlocalidad']
      actcorreo = request.POST['actcorreo']

      actualizacion = Usuarios.objects.filter(usuario__icontains=request.session['sesion']).update(nombre=actusuario, apellido=actapellido, contrasena=actcontrasena, localidad=actlocalidad, correo=actcorreo)

      actualizado = True
      
      #request.session['sesion'] = nombreusuario
      request.session['nombre'] = actusuario
      request.session['apellido'] = actapellido

      datospersona = Usuarios.objects.filter(usuario__icontains=request.session['sesion'])

      if datospersona:
         #se obtienen datos de la persona para mostrarlos en los camppos.
         for dato in datospersona:
            nombre = dato.nombre
            apellido = dato.apellido
            correo = dato.correo
            contraseña = dato.contrasena
            localidad = dato.localidad

      return render(request, "Actualizar/actUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "nusuario": nombre, "ausuario": apellido, "lusuario": localidad, "cusuario": correo, "cc": correo, "contra": contraseña,  "bandera": actualizado})

   datospersona = Usuarios.objects.filter(usuario__icontains=request.session['sesion'])

   if datospersona:
      #se obtienen datos de la persona para mostrarlos en los camppos.
       for dato in datospersona:
           nombre = dato.nombre
           apellido = dato.apellido
           correo = dato.correo
           contraseña = dato.contrasena
           localidad = dato.localidad

   


   return render(request, "Actualizar/actUsuario.html", {"nombreusuario": request.session['sesion'], "nombre": request.session['nombre'], "apellido": request.session['apellido'], "nusuario": nombre, "ausuario":apellido, "lusuario":localidad, "cusuario": correo, "cc": correo, "contra": contraseña})


def actCons(request):

   if request.method == "POST":

      nombreCons = request.POST['nombreCons']
      rutaCons = request.POST['rutaCons']
      correoCons = request.POST['correoCons']

      actualizacion = Concesionario.objects.filter(conce=request.session['conce']).update(
          nombre_conce=nombreCons, nombre_ruta=rutaCons, correo=correoCons)

      actualizado = True

      request.session['nombreconce'] = nombreCons

      datosCons = Concesionario.objects.filter(
          conce__icontains=request.session['conce'])

      rutas = Rutas.objects.all()

      if datosCons:
         #se obtienen datos de la persona para mostrarlos en los camppos.
         for dato in datosCons:
            nombrec = dato.nombre_conce
            ruta = dato.nombre_ruta
            correo = dato.correo

      return render(request, "Actualizar/actCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "nombrec": nombrec, "rutac": ruta, "correo": correo, "rutas": rutas, "actualizado":actualizado})

   datosCons = Concesionario.objects.filter(
       conce__icontains=request.session['conce'])

   rutas = Rutas.objects.all()

   if datosCons:
      #se obtienen datos de la persona para mostrarlos en los camppos.
       for dato in datosCons:
            nombrec = dato.nombre_conce
            ruta = dato.nombre_ruta
            correo = dato.correo
   
   return render(request, "Actualizar/actCons.html", {"nombreusuario": request.session['conce'], "nombre": request.session['nombreconce'], "nombrec": nombrec, "rutac": ruta, "correo": correo, "rutas": rutas})


def usuariosAdmin(request):

   usuarios=True

   listaUsuarios = Usuarios.objects.all()

   return render(request, "Administrador/usuariosAdmin.html", {"usuarios":usuarios, "listaUsuarios":listaUsuarios, })

"""Bustop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Bustop.view import prueba, login, registro, olvido, principalUsuario, buscarRuta, ubicacionRuta, mapaRutaGomez, mapaRutaTorreon, mapaRutaLerdo, quejaUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prueba/', prueba),
    path('login/', login),
    path('registro/', registro),
    path('olvido/', olvido),
    path('principalUsuario/', principalUsuario),
    path('buscarRuta/', buscarRuta),
    path('ubicacionRuta/', ubicacionRuta),
    path('mapaRutaGomez/', mapaRutaGomez),
    path('mapaRutaTorreon/', mapaRutaTorreon),
    path('mapaRutaLerdo/', mapaRutaLerdo),
    path('quejaUsuario/', quejaUsuario),
]

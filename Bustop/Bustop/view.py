from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render

def prueba(request):

    persona = "Gabriel es puto"

    return render(request, "Principal/padrePrincipal.html", {"variable": persona})

def login(request):

    persona = "Gabriel es puto"
    
    return render(request, "Principal/login.html", {"variable": persona})




from django.shortcuts import render
from django.http import HttpResponse
from agregar.models import Departamento
from agregar.models import Municipio

# Create your views here.

"""
Filtrar Datos/
Iniciar Sesion/
"""
departamentos = Departamento.objects.all()
municipios = Municipio.objects.all()

def filtrar(request):
    return render(request, "core/filtrar.html",{'departamentos':departamentos, 'municipios':municipios})

def iniciar(request):
    return render(request, "core/iniciar.html")
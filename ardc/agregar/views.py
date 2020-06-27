from django.shortcuts import render
from .models import Departamento
from .models import Municipio

# Create your views here.
def agregar(request):
    departamentos = Departamento.objects.all()
    municipios = Municipio.objects.all()
    return render(request, "agregar/agregar.html",{'departamentos':departamentos, 'municipios':municipios})
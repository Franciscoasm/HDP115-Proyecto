from django.shortcuts import render
from django.http import HttpResponse
from .models import Departamento, Municipio, Beneficio, Benefactor, Beneficiario
from .forms import FormFiltrar

# Create your views here.
"""
Filtrar Datos/
Iniciar Sesion/
Agregar Informacion/
"""
departamentos = Departamento.objects.all()
municipios = Municipio.objects.all()
ayudas = Beneficio.objects.all()
entidades = Benefactor.objects.all()
beneficiarios = Beneficiario.objects.raw('SELECT idBeneficiario, nombre_benefactor, nombre_beneficio, nombre_departamento, nombre_municipio, COUNT(idBeneficiario) AS cantidad '\
                                        'FROM core_beneficiario, core_benefactor, core_beneficio, core_municipio, core_departamento '\
                                        'WHERE core_beneficiario.benefactor_id=core_benefactor.idBenefactor '\
                                        'AND core_beneficiario.beneficio_id=core_beneficio.idBeneficio  '\
                                        'AND core_beneficiario.municipio_id=core_municipio.idMunicipio '\
                                        'AND core_beneficiario.departamento_id=core_departamento.idDepartamento '\
                                        'GROUP BY nombre_benefactor, nombre_beneficio, nombre_departamento, nombre_municipio'
)

def filtrar(request):
    form = FormFiltrar()
    if request.method == 'POST':
        form = FormFiltrar(request.POST)
        if form.is_valid():
            # Guardar los datos
            #url = reverse('home')
            return HttpResponseRedirect(url)
    return render(request, "core/filtrar.html",{'form':form, 'ayudas':ayudas, 'entidades':entidades, 'beneficiarios':beneficiarios})


def iniciar(request):
    return render(request, "core/iniciar.html")


def agregar(request):
    return render(request, "core/agregar.html")
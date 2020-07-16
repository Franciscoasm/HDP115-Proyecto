from django.shortcuts import render
from django.http import HttpResponse
from .models import Departamento, Municipio, Beneficio, Benefactor, Beneficiario, DetalleBeneficiario
from .forms import FormFiltrar
from django.db import connection
from django.shortcuts import redirect

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

def filtrar(request):

    beneficiarios = Beneficiario.objects.raw('SELECT idBeneficiario, direccion, nombre_departamento, nombre_municipio, COUNT(idBeneficiario) AS cantidad '\
                                        'FROM core_beneficiario, core_municipio, core_departamento, core_detallebeneficiario  '\
                                        'WHERE core_beneficiario.municipio_id=core_municipio.idMunicipio  '\
                                        'AND core_beneficiario.departamento_id=core_departamento.idDepartamento  '\
                                        'AND core_beneficiario.idBeneficiario=core_detallebeneficiario.beneficiario_id '\
                                        'GROUP BY direccion, nombre_departamento, nombre_municipio')
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
    form=FormFiltrar()
    if request.method=="POST":
        #creacion de objetos
        beneficiario=Beneficiario()       
        
        direccion=request.POST['direccion']
        #Como para tener identificados los datos y que se van a guardar en la tabla
        beneficiario.direccion=direccion
        
        #QuerySets que lee de la base de datos
        municipio=Municipio.objects.get(idMunicipio=request.POST['municipio']) #Consigue un objeto que tenga cualquier id del municipio
        departamento=Departamento.objects.get(idDepartamento=request.POST['departamento'])
        beneficiario.departamento=departamento
        beneficiario.municipio=municipio      
        #Guarda en la base de datos
        beneficiario.save()

        return redirect('../detalle/')

        #Combobox
        form=FormFiltrar(request.POST)
        if form.is_valid():
            return HttpResponse(url)  
   
   
    return render(request, "core/agregar.html",{'form':form})

def detalleBeneficiario(request):
    ayudas = Beneficio.objects.all()
    entidades = Benefactor.objects.all()

    detalle=DetalleBeneficiario()
    idBenefic = 0
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario WHERE estado = 1 GROUP BY idBeneficiario'
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario
    
    if results:

        if request.method=="POST":
            detalle.beneficio=Beneficio.objects.get(idBeneficio=str(request.POST['ayuda']))
            detalle.benefactor=Benefactor.objects.get(idBenefactor=str(request.POST['entidades']))
            detalle.beneficiario=Beneficiario.objects.get(idBeneficiario=str(idBenefic))
            detalle.cantidad=request.POST['cantidad']

            detalle.save()
        
        return render(request, "core/agregar-detalle.html",{'ayudas':ayudas, 'entidades':entidades})

    else :
        return redirect('/')


def actualizar(request):
    idBenefic = 0
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario GROUP BY idBeneficiario'
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario
    
    with connection.cursor() as cursor:
        cursor.execute("UPDATE core_beneficiario SET estado = 0 WHERE idBeneficiario = %s", [idBenefic])

    return redirect('/')
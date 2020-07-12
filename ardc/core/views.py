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
 
    
    
    form=FormFiltrar()
    if request.method=="POST":
        #creacion de objetos
        beneficiario=Beneficiario()
        beneficio=Beneficio()

    	#consulta
        #beneficio=Beneficio.objects.get(idBeneficio=request.POST['viveres_input'])
        #beneficio=Beneficio.objects.get(idBeneficio=request.POST['medicamento_input'] 
        beneficiario.beneficio=Beneficio.objects.get(idBeneficio=str(request.POST['ayuda']))
        beneficiario.benefactor=Benefactor.objects.get(idBenefactor=str(request.POST['entidades']))
        #beneficio1 = request.POST.get('dinero_input2','Off')
        #beneficio2=request.POST.get('viveres_input','Off')
        #beneficio3=request.POST.get('medicamento_input','Off')
    
        '''
        if(beneficio1=='on'):
             beneficio1=1
             print ("valor del input")
             print(beneficio1)
        else:
                 
                 if(beneficio2=='on'):
                     beneficio2=1
                 #print("valor del input")
                 #print(beneficio2)
                 
                 else:
                     #beneficio2=0
                         if(beneficio3=='on'):
                             beneficio3=1
                            #print("valor del input")
                            #print(beneficio3)
                         else:
                             beneficio3=0 
        '''
        
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

        #Combobox
        form=FormFiltrar(request.POST)
        if form.is_valid():
            return HttpResponse(url)  
   
   
    return render(request, "core/agregar.html",{'form':form})
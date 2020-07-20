from django.shortcuts import render
from django.http import HttpResponse
from .models import Departamento, Municipio, Beneficio, Benefactor, Beneficiario, DetalleBeneficiario
from .forms import FormFiltrar
from django.db import connection


from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm #Crea un login a partir de django
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.shortcuts import redirect

# Create your views here.
"""
Filtrar Datos/
Iniciar Sesion/
Agregar Informacion/
"""

#Obtiene todos los registros de un modelo 
departamentos = Departamento.objects.all()
municipios = Municipio.objects.all()
ayudas = Beneficio.objects.all()
entidades = Benefactor.objects.all()

def filtrar(request): #request:es la peticion
   #Obtiene los objetos de la base de datos 
    beneficiarios = Beneficiario.objects.raw('SELECT idBeneficiario, direccion, nombre_departamento, nombre_municipio, COUNT(idBeneficiario) AS cantidad '\
                                        'FROM core_beneficiario, core_municipio, core_departamento, core_detallebeneficiario  '\
                                        'WHERE core_beneficiario.municipio_id=core_municipio.idMunicipio  '\
                                        'AND core_beneficiario.departamento_id=core_departamento.idDepartamento  '\
                                        'AND core_beneficiario.idBeneficiario=core_detallebeneficiario.beneficiario_id '\
                                        'GROUP BY direccion, nombre_departamento, nombre_municipio, idBeneficiario')
    #Obtiene los objetos de la base de datos para el grafico 
    grafico = Departamento.objects.raw('SELECT idDepartamento, nombre_departamento, count(departamento_id) cont FROM core_departamento  '\
                                        'left outer join core_beneficiario on core_beneficiario.departamento_id = core_departamento.idDepartamento  '\
                                        'left join core_detallebeneficiario on core_beneficiario.idBeneficiario = core_detallebeneficiario.beneficiario_id '\
                                        'group by nombre_departamento, idDepartamento '\
                                        'order by nombre_departamento ASC')
    #Formulario
    form = FormFiltrar()
    if request.method == 'POST': #Si hace una peticion hace un cambio en la base de datos
        form = FormFiltrar(request.POST)
        if form.is_valid(): # si el formulario es valido
            # Guardar los datos
            #url = reverse('home')
            return HttpResponseRedirect(url) #redireccione 
    return render(request, "core/filtrar.html",{'form':form, 'ayudas':ayudas, 'entidades':entidades, 'beneficiarios':beneficiarios, 'grafico':grafico})


#def iniciar(request):
#    return render(request, "core/iniciar.html")


def agregar(request):
    form=FormFiltrar()
    idBenefic = 0
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario WHERE estado = 1 GROUP BY idBeneficiario'
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario

    if  results:
        return redirect('../detalle/')
    else:
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

            # Añadimos los datos recibidos al formulario
            form=FormFiltrar(request.POST)
            if form.is_valid():
                return HttpResponse(url)  #devuelve un codigo (html)
    
    #me devuelve la peticion y la template  donde muestro el contexto
        return render(request, "core/agregar.html",{'form':form})

def detalleBeneficiario(request):
    #Obteniendo los objetos de ayuda y entidades 
    ayudas = Beneficio.objects.all()
    entidades = Benefactor.objects.all()
    
    #Crea Objeto detalle beneficiario
    detalle=DetalleBeneficiario()
    idBenefic = 0
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario WHERE estado = 1 GROUP BY idBeneficiario'
     #Devuelve los objetos de la base de datos 
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario
    
    if results:

        if request.method=="POST":
            #Querysets que lee de la base de datos 
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
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario WHERE estado = 1 GROUP BY idBeneficiario'
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario
    
    contador = 0
    consulta = 'SELECT idDetalle FROM core_detallebeneficiario WHERE beneficiario_id = %s' % (idBenefic)
    results2 = DetalleBeneficiario.objects.raw(consulta)
    for result in results2:
        contador += 1
    
    if contador == 0:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_beneficiario WHERE idBeneficiario = %s", [idBenefic])
    else:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE core_beneficiario SET estado = 0 WHERE idBeneficiario = %s", [idBenefic])

    return redirect('/')

#Esta funcion lo que hace es crear el login del ususario encuestador 
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else :
        # Creamos el formulario de autenticación vacío
        form = AuthenticationForm()
        if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = AuthenticationForm(data=request.POST)
            # Si el formulario es válido...
            if form.is_valid():
                # Recuperamos las credenciales validadas
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Verificamos las credenciales del usuario
                user = authenticate(username=username, password=password)

                # Si existe un usuario con ese nombre y contraseña
                if user is not None:
                    # Hacemos el login manualmente
                    do_login(request, user)
                    # Y le redireccionamos a la portada
                    return redirect('../')

        # Si llegamos al final renderizamos el formulario
        return render(request, "core/iniciar.html", {'form': form})

def logout(request): #Cerrar Sesion
    # Redireccionamos a la portada
    do_logout(request)
    return redirect('/')

from django.shortcuts import render
from django.http import HttpResponse
from .models import Departamento, Municipio, Beneficio, Benefactor, Beneficiario
from .forms import FormFiltrar


from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
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


#def iniciar(request):
#    return render(request, "core/iniciar.html")


def agregar(request):
 
    
    
    form=FormFiltrar()
    if request.method=="POST":
        #creacion de objetos
        beneficiario=Beneficiario()
        beneficio=Beneficio()

    	#consulta para las entidades y ayuda
         
        beneficiario.beneficio=Beneficio.objects.get(idBeneficio=str(request.POST['ayuda']))
        beneficiario.benefactor=Benefactor.objects.get(idBenefactor=str(request.POST['entidades']))  
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

def logout(request):
    # Redireccionamos a la portada
    do_logout(request)
    return redirect('/')

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "core/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('../iniciar')
from django.http import JsonResponse

from .models import Departamento, Municipio, Beneficiario, DetalleBeneficiario



"""
Obtiene los municipios 
Obtiene el id del departamento, luego hace un clean con .none() borra objetos de tipo municipio
guarda la opcion seleccionada
Segun el id del departamento los municipios se van a filtrar
y se va a llenar el combobox de municipios segun el departamento que elegi 
"""
def get_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    municipios = Municipio.objects.none()
    options = '<option value="" selected="selected">-------</option>'
    if departamento_id:
        municipios = Municipio.objects.filter(departamento_id=departamento_id)   
    for municipio in municipios:
        options += '<option value="%s">%s</option>' % (
            municipio.pk,
            municipio.nombre_municipio
        )
    response = {}
    response['municipios'] = options
    return JsonResponse(response)

"""
Este funciona para filtrar segun departamento
primero obtiene el id de partamento y municipio, luego hace una consulta donde obtiene el idBeneficiario la direccion
nombre del departamento y municipio donde cuenta el id del beneficiario ya que un usuario puede ingresar mas de una ayuda
y eso va a traerlo de las tablas siguientes, y eso solo puede hacerse si el idMunicipio es igual el del departamento
el de beneficiario, luego agrega un string ya sea de departamento o municipio, agrupa los datos segun los campos 
que le proporciono, luego crea una tabla con algunos campos y uno de detalle y otro de cantidad
Devuelve los registros de la base de datos para crear una ventana flotante donde se puede ver la direccion, el nombre municipio,
cantidad departamento id beneficiario, si no encuentra los registros al filtrar mostrara un error y la tabla no se mostrara 
"""



def get_info(request):
    control = 0
    departamento_id = request.GET.get('departamento_id')
    municipio_id = request.GET.get('municipio_id')

    consulta = 'SELECT idBeneficiario, direccion, nombre_departamento, nombre_municipio, COUNT(idBeneficiario) AS cantidad '\
                'FROM core_beneficiario, core_municipio, core_departamento, core_detallebeneficiario  '\
                'WHERE core_beneficiario.municipio_id=core_municipio.idMunicipio  '\
                'AND core_beneficiario.departamento_id=core_departamento.idDepartamento  '\
                'AND core_beneficiario.idBeneficiario=core_detallebeneficiario.beneficiario_id '
    if departamento_id:
        consulta += ' AND core_beneficiario.departamento_id = %s' % (departamento_id) 
    if municipio_id:
        consulta += ' AND core_beneficiario.municipio_id = %s' % (municipio_id) 
    
    consulta += ' GROUP BY direccion, nombre_departamento, nombre_municipio, idBeneficiario '

    table = '<table class="table table-hover">'\
                '<thead>'\
                    '<tr class="table-primary">'\
                    '<th scope="col">Direccion</th>'\
                        '<th scope="col">Departamento</th>'\
                        '<th scope="col">Municipio</th>'\
                        '<th scope="col">Cantidad de Ayudas</th>'\
                        '<th scope="col">Detalle</th>'\
                    '</tr>'\
                '</thead>'\
                '<tbody>'
    beneficiarios = Beneficiario.objects.raw(consulta)
    for beneficiario in beneficiarios:
        control += 1
        table+= '<tr class="table-light">'\
                    '<td>%s</td>'\
                    '<td>%s</td>'\
                    '<td>%s</td>'\
                    '<td>%s</td>'\
                    '<td>'\
                        '<button type="button" onclick="getInfoExtend(%s)" class="btn btn-link" data-toggle="modal" data-target="#exampleModal">'\
                            '<i class="large material-icons">more</i>'\
                        '</button>'\
                    '</td>'\
                '</tr>' % (
            beneficiario.direccion,
            beneficiario.nombre_departamento,
            beneficiario.nombre_municipio,
            beneficiario.cantidad,
            beneficiario.idBeneficiario,
        )
    if control == 0 :
        table = '<div class="alert alert-dismissible alert-warning">'\
                    '<h4 class="alert-heading">¡Atención!</h4>'\
                    '<p class="mb-0">No se han encontrado registros</p>'\
                '</div>'
    else :
        table += '</tbody></table>'
    response2 = {}
    response2['beneficiarios'] = table
    return JsonResponse(response2)

def get_last(request):
    #Obtener el ultimo id
    idBenefic = 0
    consulta = 'SELECT idBeneficiario, MAX(idBeneficiario) id FROM core_beneficiario GROUP BY idBeneficiario'
    results = Beneficiario.objects.raw(consulta)
    for result in results:
        idBenefic = result.idBeneficiario
    response = {}
    response['idLast'] = idBenefic
    return JsonResponse(response)


"""
ventana flotante, se necesita hacer una consulta para ver los datos segun direccion depa y municipio segun el id del beneficiario
guardando los datos en consulta, agrega una tabla, se obtienen los datos de la base de datos 
de la tabla detalle beneficiario y cada ves que se ingresen essos datos se creara la tabla, si no hay datos mostrara un error
"""

def get_detalle(request):
    control = 0
    id_beneficiario = request.GET.get('beneficiario_id')
    consulta = 'SELECT idDetalle, nombre_beneficio, nombre_benefactor, cantidad FROM core_detallebeneficiario AS detalle '\
                'inner join core_beneficiario AS beneficiario ON detalle.beneficiario_id = beneficiario.idBeneficiario '\
                'inner join core_beneficio AS beneficio ON detalle.beneficio_id = beneficio.idBeneficio '\
                'inner join core_benefactor AS benefactor ON detalle.benefactor_id = benefactor.idBenefactor '\
                'WHERE detalle.beneficiario_id = '
    consulta += id_beneficiario
    table = '<table class="table table-hover">'\
                '<thead>'\
                    '<tr class="table-primary">'\
                        '<th scope="col">Tipo de Ayuda</th>'\
                        '<th scope="col">Cantidad</th>'\
                        '<th scope="col">Entidad</th>'\
                    '</tr>'\
                '</thead>'\
                '<tbody>'
    detalles = DetalleBeneficiario.objects.raw(consulta)
    for detalle in detalles:
        control += 1
        table+= '<tr class="table-light">'\
                    '<td>%s</td>'\
                    '<td>%s</td>'\
                    '<td>%s</td>'\
                '</tr>' % (
            detalle.nombre_beneficio,
            detalle.cantidad,
            detalle.nombre_benefactor,
        )
    if control == 0 :
        table = '<div class="alert alert-dismissible alert-warning">'\
                    '<h4 class="alert-heading">¡Atención!</h4>'\
                    '<p class="mb-0">No se han encontrado registros</p>'\
                '</div>'
    else :
        table += '</tbody></table>'
    response = {}
    response['detallesExtend'] = table
    return JsonResponse(response)
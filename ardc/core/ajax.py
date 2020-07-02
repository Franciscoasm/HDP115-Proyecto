from django.http import JsonResponse

from .models import Departamento, Municipio, Beneficiario


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

def get_info(request):
    control = 0
    departamento_id = request.GET.get('departamento_id')
    municipio_id = request.GET.get('municipio_id')
    beneficio_id = request.GET.get('beneficio_id')
    benefactor_id = request.GET.get('benefactor_id')

    consulta = 'SELECT idBeneficiario, nombre_benefactor, nombre_beneficio, nombre_departamento, nombre_municipio, COUNT(idBeneficiario) AS cantidad '\
                'FROM core_beneficiario, core_benefactor, core_beneficio, core_municipio, core_departamento '\
                'WHERE core_beneficiario.benefactor_id=core_benefactor.idBenefactor '\
                'AND core_beneficiario.beneficio_id=core_beneficio.idBeneficio  '\
                'AND core_beneficiario.municipio_id=core_municipio.idMunicipio '\
                'AND core_beneficiario.departamento_id=core_departamento.idDepartamento'
    if departamento_id:
        consulta += ' AND core_beneficiario.departamento_id = %s' % (departamento_id) 
    if municipio_id:
        consulta += ' AND core_beneficiario.municipio_id = %s' % (municipio_id) 
    if beneficio_id:
        consulta += ' AND core_beneficiario.beneficio_id = %s' % (beneficio_id) 
    if benefactor_id:
        consulta += ' AND core_beneficiario.benefactor_id = %s' % (benefactor_id) 
    
    consulta += ' GROUP BY nombre_benefactor, nombre_beneficio, nombre_departamento, nombre_municipio'

    table = '<table class="table table-hover">'\
                '<thead>'\
                    '<tr class="table-primary">'\
                        '<th scope="col">Departamento</th>'\
                        '<th scope="col">Municipio</th>'\
                        '<th scope="col">Tipo de ayuda</th>'\
                        '<th scope="col">Entidad</th>'\
                        '<th scope="col">Cantidad</th>'\
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
                    '<td>%s</td>'\
                '</tr>' % (
            beneficiario.nombre_departamento,
            beneficiario.nombre_municipio,
            beneficiario.nombre_beneficio,
            beneficiario.nombre_benefactor,
            beneficiario.cantidad,
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
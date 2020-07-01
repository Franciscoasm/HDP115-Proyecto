from django.http import JsonResponse

from .models import Departamento
from .models import Municipio


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
from django.contrib import admin
from .models import Departamento
from .models import Municipio
from .models import Usuario

# Register your models here.

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Usuario)

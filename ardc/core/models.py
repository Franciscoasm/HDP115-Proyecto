from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class Departamento(models.Model):
    idDepartamento = models.CharField(max_length=10,primary_key=True)
    nombre_departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_departamento

class Municipio(models.Model):
    idMunicipio = models.CharField(max_length=10,primary_key=True)
    departamento = models.ForeignKey(Departamento, null = True, blank = True, on_delete=models.CASCADE)
    nombre_municipio = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre_municipio

class Usuario(models.Model):
    idUsuario = models.CharField(max_length=10,primary_key=True)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre_usuario = models.CharField(max_length=50)
    contraseña=models.CharField(max_length=50, default='SOME STRING')
    institucion = models.CharField(max_length=50)


class Benefactor(models.Model):
    idBenefactor = models.CharField(max_length=10,primary_key=True)
    nombre_benefactor = models.CharField(max_length=50)

class Beneficio(models.Model):
    idBeneficio = models.CharField(max_length=10,primary_key=True)
    nombre_beneficio = models.CharField(max_length=50)

class Beneficiario(models.Model):
    idBeneficiario = models.AutoField(primary_key=True)
    direccion=models.CharField(max_length=50, default='SOME STRING')
    departamento = models.ForeignKey(Departamento, null = True, blank = True, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, null = True, blank = True, on_delete=models.CASCADE)   
    beneficio = models.ForeignKey(Beneficio, null = True, blank = True, on_delete=models.CASCADE)
    benefactor = models.ForeignKey(Benefactor, null = True, blank = True, on_delete=models.CASCADE)




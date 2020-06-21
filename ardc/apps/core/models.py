from django.db import models

# Create your models here.

class Departamento(models.Model):
    #idDepartamento = models.CharField(max_length=10,primary_key=True)
    nombre_departamento = models.CharField(max_length=50)

class Municipio(models.Model):
    #idMunicipio = models.CharField(max_length=10,primary_key=True)
    departamento = models.ForeignKey(Departamento, null = True, blank = True, on_delete=models.CASCADE)
    nombre_municipio = models.CharField(max_length=50)

class Usuario(models.Model):
    #idUsuario = models.CharField(max_length=10,primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    institucion = models.CharField(max_length=50)

class Beneficiario(models.Model):
    #idBeneficiario = models.CharField(max_length=10,primary_key=True)
    departameto = models.ForeignKey(Departamento, null = True, blank = True, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, null = True, blank = True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null = True, blank = True, on_delete=models.CASCADE)

class Benefactor(models.Model):
    #idBenefactor = models.CharField(max_length=10,primary_key=True)
    nombre_benefactor = models.CharField(max_length=50)

class Beneficio(models.Model):
    #idBeneficio = models.CharField(max_length=10,primary_key=True)
    nombre_beneficio = models.CharField(max_length=50)
    benefactor = models.ForeignKey(Benefactor, null = True, blank = True, on_delete=models.CASCADE)
    beneficiario = models.ForeignKey(Beneficiario, null = True, blank = True, on_delete=models.CASCADE)

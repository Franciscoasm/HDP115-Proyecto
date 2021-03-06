# Generated by Django 3.0.8 on 2020-07-01 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefactor',
            fields=[
                ('idBenefactor', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_benefactor', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Beneficio',
            fields=[
                ('idBeneficio', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_beneficio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('idDepartamento', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_departamento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('institucion', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('idMunicipio', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_municipio', models.CharField(max_length=50)),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Beneficiario',
            fields=[
                ('idBeneficiario', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('benefactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Benefactor')),
                ('beneficio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Beneficio')),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Departamento')),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Municipio')),
            ],
        ),
    ]

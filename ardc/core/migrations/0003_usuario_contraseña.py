# Generated by Django 3.0.7 on 2020-07-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200712_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='contraseña',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
    ]
